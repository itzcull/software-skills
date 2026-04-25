# E2E and Browser Testing

End-to-end tests verify that the whole system works for real users. Component tests verify that UI components work correctly.

## Scope and Philosophy

### What E2E Tests Should Cover

E2E tests verify critical user journeys through real entry points:

| Should Test | Should NOT Test |
|-------------|-----------------|
| Complete user flows (login → purchase → confirmation) | Every edge case |
| Critical happy paths | Business logic details |
| Cross-system integration | Third-party dependencies |
| User-observable outcomes | Internal state changes |

### Component Testing Philosophy

> "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

Test user-visible behavior, not component internals:

```typescript
// ❌ BAD - Testing implementation details
it("should set openIndex state to 1 when clicking header", () => {
  const wrapper = mount(<Accordion items={items} />);
  wrapper.instance().setOpenIndex(1);
  expect(wrapper.state("openIndex")).toBe(1);
});

// ✅ GOOD - Testing user-visible behavior
it("should show item contents when header is clicked", async () => {
  render(<Accordion items={items} />);

  expect(screen.queryByText(items[1].contents)).not.toBeInTheDocument();

  await userEvent.click(screen.getByText(items[1].title));

  expect(screen.getByText(items[1].contents)).toBeInTheDocument();
});
```

## Testing Library Query Priority

Testing Library provides prioritized queries that match how users find elements:

### Query Priority (Highest to Lowest)

| Priority | Query | Use Case | Example |
|----------|-------|----------|---------|
| 1 | `getByRole` | Interactive elements | `getByRole('button', { name: 'Submit' })` |
| 2 | `getByLabelText` | Form fields | `getByLabelText('Email Address')` |
| 3 | `getByPlaceholderText` | When no label exists | `getByPlaceholderText('Enter your email')` |
| 4 | `getByText` | Non-interactive elements | `getByText('Welcome, John')` |
| 5 | `getByDisplayValue` | Filled form values | `getByDisplayValue('john@example.com')` |
| 6 | `getByAltText` | Images | `getByAltText('Product photo')` |
| 7 | `getByTitle` | Tooltips (inconsistent) | `getByTitle('Delete item')` |
| 8 | `getByTestId` | Last resort | `getByTestId('submit-button')` |

### Why This Order?

- **Role/Text**: How users navigate
- **Accessibility**: How assistive technology works
- **Resilience**: Survives styling changes

```typescript
// ✅ GOOD - Priority-based queries
describe("LoginForm", () => {
  it("should authenticate user", async () => {
    render(<LoginForm />);

    // Role-based for button
    const submitButton = screen.getByRole("button", { name: /sign in/i });

    // Label-based for input
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    await userEvent.type(emailInput, "user@example.com");
    await userEvent.type(passwordInput, "password123");
    await userEvent.click(submitButton);

    expect(await screen.findByText(/welcome/i)).toBeInTheDocument();
  });
});

// ❌ BAD - Fragile selectors
screen.getByTestId("login-submit-button"); // Brittle, hidden from users
screen.getByCss("button.btn-primary"); // Breaks on style changes
```

## Playwright Best Practices

### Locator Strategies

Prefer user-facing locators over DOM-based ones:

```typescript
// ✅ GOOD - User-facing locators
page.getByRole("button", { name: "Submit payment" });
page.getByLabelText("Email address");
page.getByText("Order confirmed");
page.getByPlaceholderText("Enter amount");

// ❌ BAD - DOM-based locators
page.locator("button.btn-primary"); // Style-dependent
page.locator(".payment-form button:nth-child(2)"); // Position-dependent
page.locator('[data-testid="submit"]'); // Last resort
```

### Chaining and Filtering

Narrow down locators by context:

```typescript
// Filter by text
const productRow = page.getByRole("listitem").filter({ hasText: "Product 2" });
await productRow.getByRole("button", { name: "Add to cart" }).click();

// Chain locators for specificity
await page
  .getByRole("form", { name: "Checkout" })
  .getByLabelText("Card number")
  .fill("4242424242424242");
```

### Web-First Assertions

Use Playwright's auto-waiting assertions:

```typescript
// ✅ GOOD - Web-first assertions with auto-wait
await expect(page.getByText("Order confirmed")).toBeVisible();
await expect(page.getByRole("alert")).toHaveText(/payment successful/i);
await expect(page.locator(".total")).toContainText("$150.00");

// ❌ BAD - Manual assertions without waiting
expect(await page.getByText("Order confirmed").isVisible()).toBe(true);
```

### Auto-Waiting

Playwright automatically waits for elements to be actionable:

```typescript
// Playwright waits automatically:
// - Element is visible
// - Element is enabled
// - Element is stable (not animating)
// - No overlay blocking
// - Element is in DOM

// Manual waiting when needed
await page.waitForSelector(".loading-spinner", { state: "hidden" });
await page.waitForLoadState("networkidle");
```

### Handling Async Behavior

```typescript
// Using findBy for async elements
const loadingIndicator = screen.getByText(/loading/i);
// Don't assert it's visible, wait for it to disappear
await expect(loadingIndicator).not.toBeVisible();

// Waiting for API calls
await page.waitForResponse(/api\/orders/);
await page.waitForResponse((response) => response.url().includes("/orders"));

// Waiting for navigation
await page.waitForURL("**/confirmation/**");
```

## userEvent vs fireEvent

### When to Use Each

| API | Use Case |
|-----|----------|
| `userEvent` | Default choice — simulates real user behavior |
| `fireEvent` | Low-level, when userEvent is insufficient |

### userEvent API

```typescript
import userEvent from "@testing-library/user-event";

// Typing into inputs
await userEvent.type(screen.getByLabelText("Email"), "user@example.com");

// Clicking (realistic behavior)
await userEvent.click(screen.getByRole("button", { name: "Submit" }));

// Hover and focus
await userEvent.hover(screen.getByTestId("tooltip-trigger"));
await userEvent.focus(screen.getByLabelText("Username"));

// Selecting options
await userEvent.selectOptions(screen.getByRole("combobox"), ["option-2"]);

// Tab navigation
await userEvent.tab();

// Clipboard
await userEvent.copy();
await userEvent.paste("text");
```

### When to Use fireEvent

```typescript
import { fireEvent } from "@testing-library/react";

// Custom events
fireEvent.customEvent(window, "custom-event", { detail: "data" });

// When userEvent doesn't support the interaction
fireEvent.mouseEnter(element);
fireEvent.mouseLeave(element);

// Form submit without button click
fireEvent.submit(screen.getByRole("form"));
```

## Component Testing Patterns

### Testing Async Components

```typescript
describe("UserProfile component", () => {
  it("should display user data after loading", async () => {
    // Mock the API call
    jest.spyOn(api, "getUser").mockResolvedValue({
      id: "1",
      name: "Alice",
      email: "alice@example.com",
    });

    render(<UserProfile userId="1" />);

    // Initially shows loading
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // After data loads, shows user info
    expect(await screen.findByText("Alice")).toBeInTheDocument();
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it("should show error when user not found", async () => {
    jest.spyOn(api, "getUser").mockRejectedValue(new Error("User not found"));

    render(<UserProfile userId="999" />);

    expect(await screen.findByText(/user not found/i)).toBeInTheDocument();
  });
});
```

### Testing Forms

```typescript
describe("CheckoutForm", () => {
  it("should validate required fields", async () => {
    render(<CheckoutForm onSubmit={jest.fn()} />);

    await userEvent.click(screen.getByRole("button", { name: /place order/i }));

    expect(screen.getByLabelText(/card number/i)).toHaveErrorMessage(/required/i);
    expect(screen.getByLabelText(/expiry/i)).toHaveErrorMessage(/required/i);
  });

  it("should submit valid form data", async () => {
    const onSubmit = jest.fn();
    render(<CheckoutForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/card number/i), "4242424242424242");
    await userEvent.type(screen.getByLabelText(/expiry/i), "12/25");
    await userEvent.type(screen.getByLabelText(/cvv/i), "123");
    await userEvent.click(screen.getByRole("button", { name: /place order/i }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        cardNumber: "4242424242424242",
        expiry: "12/25",
        cvv: "123",
      })
    );
  });
});
```

### Testing Error States

```typescript
describe("PaymentForm error handling", () => {
  it("should display API error message", async () => {
    jest.spyOn(paymentApi, "processPayment").mockRejectedValue(
      new Error("Insufficient funds")
    );

    render(<PaymentForm />);
    await userEvent.click(screen.getByRole("button", { name: /pay/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/insufficient funds/i);
  });

  it("should retry after error", async () => {
    const mock = jest
      .spyOn(paymentApi, "processPayment")
      .mockRejectedValueOnce(new Error("Network error"))
      .mockResolvedValueOnce({ success: true });

    render(<PaymentForm />);

    await userEvent.click(screen.getByRole("button", { name: /pay/i }));
    await userEvent.click(screen.getByRole("button", { name: /retry/i }));

    expect(mock).toHaveBeenCalledTimes(2);
  });
});
```

## E2E Test Structure

### Page Object Model

```typescript
// pages/CheckoutPage.ts
export class CheckoutPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto("/checkout");
  }

  async fillCardNumber(cardNumber: string) {
    await this.page.getByLabelText(/card number/i).fill(cardNumber);
  }

  async fillExpiry(expiry: string) {
    await this.page.getByLabelText(/expiry/i).fill(expiry);
  }

  async fillCvv(cvv: string) {
    await this.page.getByLabelText(/cvv/i).fill(cvv);
  }

  async clickPay() {
    await this.page.getByRole("button", { name: /pay/i }).click();
  }

  async getErrorMessage() {
    return this.page.getByRole("alert").textContent();
  }

  async getConfirmationText() {
    return this.page.getByRole("heading", { name: /order confirmed/i }).textContent();
  }
}

// tests/checkout.spec.ts
import { test, expect } from "@playwright/test";
import { CheckoutPage } from "../pages/CheckoutPage";

test("successful checkout flow", async ({ page }) => {
  const checkout = new CheckoutPage(page);
  await checkout.goto();

  await checkout.fillCardNumber("4242424242424242");
  await checkout.fillExpiry("12/25");
  await checkout.fillCvv("123");
  await checkout.clickPay();

  await expect(page.getByRole("heading", { name: /order confirmed/i })).toBeVisible();
});

test("invalid card shows error", async ({ page }) => {
  const checkout = new CheckoutPage(page);
  await checkout.goto();

  await checkout.fillCardNumber("invalid");
  await checkout.clickPay();

  await expect(page.getByRole("alert")).toHaveText(/invalid card number/i);
});
```

### Test Isolation

Each test should be independent:

```typescript
// ✅ GOOD - Self-contained test
test("should create new order", async ({ page }) => {
  await page.goto("/orders/new");
  await page.fill("input[name='item']", "Widget");
  await page.click("button[type='submit']");

  await expect(page).toHaveURL(/\/orders\/\w+/);
});

// ❌ BAD - Tests depend on previous test state
let orderId: string;
test("creates order", async ({ page }) => {
  await page.goto("/orders/new");
  await page.fill("input[name='item']", "Widget");
  await page.click("button[type='submit']");
  orderId = page.url().split("/").pop()!; // Order ID for next test
});

test("edits order", async ({ page }) => {
  await page.goto(`/orders/${orderId}`); // Depends on previous test
  // This test will fail if the first test fails
});
```

### Before Each Hooks

```typescript
test.describe("Checkout flow", () => {
  test.beforeEach(async ({ page }) => {
    // Sign in for every test
    await page.goto("/login");
    await page.fill("input[name='email']", "test@example.com");
    await page.fill("input[name='password']", "password");
    await page.click("button[type='submit']");
    await page.waitForURL("/dashboard");
  });

  test("should complete purchase", async ({ page }) => {
    await page.goto("/products");
    // Test continues...
  });

  test("should show cart contents", async ({ page }) => {
    await page.goto("/cart");
    // Test continues...
  });
});
```

## Handling Third-Party Dependencies

Don't test external sites:

```typescript
// ❌ BAD - Testing external site
test("should redirect to payment provider", async ({ page }) => {
  await page.goto("/checkout");
  await page.click("button[href*='stripe.com']");

  // Now we're on Stripe's site - bad idea
  await expect(page).toHaveURL(/stripe\.com/);
});

// ✅ GOOD - Mock the redirect
test("should initiate payment flow", async ({ page }) => {
  await page.goto("/checkout");
  await page.click("button[value='stripe']");

  expect(page).toHaveURL(/^\/api\/payment-intent/);
});
```

## Parallelization and CI

### Running Tests in Parallel

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
});
```

### Sharding for CI

```bash
# Run tests across 3 machines
npx playwright test --shard=1/3
npx playwright test --shard=2/3
npx playwright test --shard=3/3
```

### Optimizing Browser Downloads

```bash
# Install only needed browsers
npx playwright install chromium

# Instead of all browsers
npx playwright install --with-deps
```

## Debugging Failed Tests

### Trace Viewer

Configure traces for failed tests:

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: "on-first-retry",
  },
});
```

Run with trace:

```bash
npx playwright test --trace on
npx playwright show-report
```

### Debug Mode

```bash
# Debug single test
npx playwright test checkout.spec.ts --debug

# Step through test
# View timeline, screenshots, network requests
```

### Soft Assertions

```typescript
import { test, expect } from "@playwright/test";

test("soft assertions collect all failures", async ({ page }) => {
  // Multiple checks, continue after first failure
  await expect.soft(page.locator("#total")).toHaveText("$100.00");
  await expect.soft(page.locator("#items")).toHaveCount(5);
  await expect.soft(page.locator(".discount")).toBeVisible();

  // Report all failures at once
});
```

## Performance Considerations

### Keep E2E Suite Fast

| Guideline | Target |
|-----------|--------|
| Single E2E test | < 30 seconds |
| E2E suite | < 10 minutes |
| Percentage of test time | < 10% of total |

### Tips for Speed

- **Use Playwright's test runner** (not manual browser automation)
- **Parallelize across browsers**
- **Shard across CI workers**
- **Skip E2E on fast commits**, run on PR merge
- **Mock expensive API calls** when possible
- **Use smaller test data**

## When to Skip E2E Tests

E2E tests are slow and brittle. Skip when:

- Unit/integration tests already cover the behavior
- The test is for an edge case rarely hit by users
- The feature is UI-only without business logic
- The test takes more than 60 seconds

## Accessibility Testing

Include a11y checks in component tests:

```typescript
import { injectAxe, checkA11y } from "axe-playwright";

describe("CheckoutForm accessibility", () => {
  it("should have no accessibility violations", async ({ page }) => {
    await page.goto("/checkout");
    await injectAxe(page);

    await checkA11y(page, {
      detailedReport: true,
      detailedReportOptions: { html: true },
    });
  });

  it("should indicate required fields", async ({ page }) => {
    await page.goto("/checkout");

    const emailInput = page.getByLabelText(/email/i);
    expect(emailInput).toHaveAttribute("aria-required", "true");
  });
});
```

## See Also

- [Test Doubles](./test-doubles.md) — Mocking philosophy
- [Integration Testing](./integration-testing.md) — Backend integration patterns
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Testing Library Queries](https://testing-library.com/docs/queries/about)
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles)
- [Kent C. Dodds: Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details)
