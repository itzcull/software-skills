---
title: "Replace Conditional with Polymorphism"
description: "Replace complex conditional logic with polymorphic method calls instead of switch statements or if-else chains"
category: "Simplifying Conditional Logic"
tags: ["polymorphism", "conditional", "inheritance", "switch", "object-oriented", "open-closed-principle"]
related: ["replace-type-code-with-subclasses", "extract-class", "replace-parameter-with-query"]
---

# Replace Conditional with Polymorphism

Replace complex conditional logic with polymorphic method calls. Instead of using switch statements or if-else chains to determine behavior, use inheritance and method overriding to let objects handle their own behavior.

## Motivation

Conditional logic based on type codes or object types creates several problems:

- **Violation of Open/Closed Principle**: Adding new types requires modifying existing conditional statements
- **Code duplication**: Same conditional logic scattered throughout the codebase
- **Hard to extend**: Adding new types becomes increasingly difficult
- **Poor encapsulation**: Business logic is separated from the data it operates on
- **Maintenance burden**: Changes to type behavior require finding all conditional statements

## Example

### Basic Example
```javascript
// Before - Conditional logic based on type
class Bird {
  constructor(type, speed) {
    this._type = type;
    this._speed = speed;
  }
  
  get type() { return this._type; }
  get speed() { return this._speed; }
  
  getAirSpeed() {
    switch (this._type) {
      case 'european_swallow':
        return 35;
      case 'african_swallow':
        return 40;
      case 'norwegian_blue':
        return 0; // It's dead
      default:
        throw new Error(`Unknown bird type: ${this._type}`);
    }
  }
  
  canFly() {
    switch (this._type) {
      case 'european_swallow':
      case 'african_swallow':
        return true;
      case 'norwegian_blue':
        return false;
      default:
        throw new Error(`Unknown bird type: ${this._type}`);
    }
  }
  
  makeSound() {
    switch (this._type) {
      case 'european_swallow':
        return 'chirp chirp';
      case 'african_swallow':
        return 'tweet tweet';
      case 'norwegian_blue':
        return ''; // It's silent
      default:
        throw new Error(`Unknown bird type: ${this._type}`);
    }
  }
}

// Usage
const europeanSwallow = new Bird('european_swallow', 35);
console.log(europeanSwallow.getAirSpeed()); // 35
console.log(europeanSwallow.canFly());      // true

// After - Polymorphic approach
class Bird {
  constructor(speed) {
    this._speed = speed;
  }
  
  get speed() { return this._speed; }
  
  // Abstract methods - subclasses must implement
  getAirSpeed() {
    throw new Error('Subclasses must implement getAirSpeed');
  }
  
  canFly() {
    throw new Error('Subclasses must implement canFly');
  }
  
  makeSound() {
    throw new Error('Subclasses must implement makeSound');
  }
}

class EuropeanSwallow extends Bird {
  constructor() {
    super(35);
  }
  
  getAirSpeed() {
    return 35;
  }
  
  canFly() {
    return true;
  }
  
  makeSound() {
    return 'chirp chirp';
  }
}

class AfricanSwallow extends Bird {
  constructor() {
    super(40);
  }
  
  getAirSpeed() {
    return 40;
  }
  
  canFly() {
    return true;
  }
  
  makeSound() {
    return 'tweet tweet';
  }
}

class NorwegianBlue extends Bird {
  constructor() {
    super(0);
  }
  
  getAirSpeed() {
    return 0; // It's resting
  }
  
  canFly() {
    return false; // It's expired
  }
  
  makeSound() {
    return ''; // It's joined the choir invisible
  }
}

// Usage
const europeanSwallow = new EuropeanSwallow();
console.log(europeanSwallow.getAirSpeed()); // 35
console.log(europeanSwallow.canFly());      // true

// Easy to add new types without modifying existing code
class Penguin extends Bird {
  constructor() {
    super(0);
  }
  
  getAirSpeed() {
    return 0;
  }
  
  canFly() {
    return false;
  }
  
  makeSound() {
    return 'squawk';
  }
  
  getSwimSpeed() {
    return 8; // km/h underwater
  }
}
```

### Complex Example - Payment Processing
```javascript
// Before - Complex conditional payment logic
class PaymentProcessor {
  processPayment(payment) {
    switch (payment.type) {
      case 'credit_card':
        return this._processCreditCard(payment);
      case 'paypal':
        return this._processPayPal(payment);
      case 'bank_transfer':
        return this._processBankTransfer(payment);
      case 'cryptocurrency':
        return this._processCryptocurrency(payment);
      default:
        throw new Error(`Unsupported payment type: ${payment.type}`);
    }
  }
  
  calculateFee(payment) {
    switch (payment.type) {
      case 'credit_card':
        return payment.amount * 0.029 + 0.30; // 2.9% + $0.30
      case 'paypal':
        return payment.amount * 0.034 + 0.30; // 3.4% + $0.30
      case 'bank_transfer':
        return payment.amount > 1000 ? 0 : 5.00; // Free for large amounts
      case 'cryptocurrency':
        return payment.amount * 0.01; // 1%
      default:
        throw new Error(`Unsupported payment type: ${payment.type}`);
    }
  }
  
  getProcessingTime(payment) {
    switch (payment.type) {
      case 'credit_card':
        return 'instant';
      case 'paypal':
        return 'instant';
      case 'bank_transfer':
        return '1-3 business days';
      case 'cryptocurrency':
        return '10-60 minutes';
      default:
        throw new Error(`Unsupported payment type: ${payment.type}`);
    }
  }
  
  validatePayment(payment) {
    switch (payment.type) {
      case 'credit_card':
        return this._validateCreditCard(payment);
      case 'paypal':
        return this._validatePayPal(payment);
      case 'bank_transfer':
        return this._validateBankTransfer(payment);
      case 'cryptocurrency':
        return this._validateCryptocurrency(payment);
      default:
        throw new Error(`Unsupported payment type: ${payment.type}`);
    }
  }
  
  _processCreditCard(payment) {
    // Credit card processing logic
    return { success: true, transactionId: 'cc_' + generateId() };
  }
  
  _processPayPal(payment) {
    // PayPal processing logic
    return { success: true, transactionId: 'pp_' + generateId() };
  }
  
  _processBankTransfer(payment) {
    // Bank transfer processing logic
    return { success: true, transactionId: 'bt_' + generateId() };
  }
  
  _processCryptocurrency(payment) {
    // Cryptocurrency processing logic
    return { success: true, transactionId: 'crypto_' + generateId() };
  }
  
  // Validation methods...
  _validateCreditCard(payment) { return true; }
  _validatePayPal(payment) { return true; }
  _validateBankTransfer(payment) { return true; }
  _validateCryptocurrency(payment) { return true; }
}

// After - Polymorphic payment processing
class PaymentMethod {
  constructor(amount) {
    this._amount = amount;
  }
  
  get amount() { return this._amount; }
  
  // Abstract methods
  process() {
    throw new Error('Subclasses must implement process');
  }
  
  calculateFee() {
    throw new Error('Subclasses must implement calculateFee');
  }
  
  getProcessingTime() {
    throw new Error('Subclasses must implement getProcessingTime');
  }
  
  validate() {
    throw new Error('Subclasses must implement validate');
  }
}

class CreditCardPayment extends PaymentMethod {
  constructor(amount, cardNumber, expiryDate, cvv) {
    super(amount);
    this._cardNumber = cardNumber;
    this._expiryDate = expiryDate;
    this._cvv = cvv;
  }
  
  process() {
    if (!this.validate()) {
      throw new Error('Invalid credit card information');
    }
    
    // Credit card specific processing
    const transactionId = 'cc_' + this._generateTransactionId();
    return {
      success: true,
      transactionId,
      fee: this.calculateFee(),
      processingTime: this.getProcessingTime()
    };
  }
  
  calculateFee() {
    return this._amount * 0.029 + 0.30; // 2.9% + $0.30
  }
  
  getProcessingTime() {
    return 'instant';
  }
  
  validate() {
    return this._cardNumber && 
           this._expiryDate && 
           this._cvv && 
           this._cardNumber.length === 16;
  }
  
  _generateTransactionId() {
    return Math.random().toString(36).substr(2, 9);
  }
}

class PayPalPayment extends PaymentMethod {
  constructor(amount, email, password) {
    super(amount);
    this._email = email;
    this._password = password;
  }
  
  process() {
    if (!this.validate()) {
      throw new Error('Invalid PayPal credentials');
    }
    
    // PayPal specific processing
    const transactionId = 'pp_' + this._generateTransactionId();
    return {
      success: true,
      transactionId,
      fee: this.calculateFee(),
      processingTime: this.getProcessingTime()
    };
  }
  
  calculateFee() {
    return this._amount * 0.034 + 0.30; // 3.4% + $0.30
  }
  
  getProcessingTime() {
    return 'instant';
  }
  
  validate() {
    return this._email && 
           this._password && 
           this._email.includes('@');
  }
  
  _generateTransactionId() {
    return Math.random().toString(36).substr(2, 9);
  }
}

class BankTransferPayment extends PaymentMethod {
  constructor(amount, accountNumber, routingNumber) {
    super(amount);
    this._accountNumber = accountNumber;
    this._routingNumber = routingNumber;
  }
  
  process() {
    if (!this.validate()) {
      throw new Error('Invalid bank account information');
    }
    
    // Bank transfer specific processing
    const transactionId = 'bt_' + this._generateTransactionId();
    return {
      success: true,
      transactionId,
      fee: this.calculateFee(),
      processingTime: this.getProcessingTime()
    };
  }
  
  calculateFee() {
    return this._amount > 1000 ? 0 : 5.00; // Free for large amounts
  }
  
  getProcessingTime() {
    return '1-3 business days';
  }
  
  validate() {
    return this._accountNumber && 
           this._routingNumber && 
           this._accountNumber.length >= 8;
  }
  
  _generateTransactionId() {
    return Math.random().toString(36).substr(2, 9);
  }
}

class CryptocurrencyPayment extends PaymentMethod {
  constructor(amount, walletAddress, privateKey, currency = 'BTC') {
    super(amount);
    this._walletAddress = walletAddress;
    this._privateKey = privateKey;
    this._currency = currency;
  }
  
  process() {
    if (!this.validate()) {
      throw new Error('Invalid cryptocurrency wallet information');
    }
    
    // Cryptocurrency specific processing
    const transactionId = 'crypto_' + this._generateTransactionId();
    return {
      success: true,
      transactionId,
      fee: this.calculateFee(),
      processingTime: this.getProcessingTime(),
      currency: this._currency
    };
  }
  
  calculateFee() {
    return this._amount * 0.01; // 1%
  }
  
  getProcessingTime() {
    return '10-60 minutes';
  }
  
  validate() {
    return this._walletAddress && 
           this._privateKey && 
           this._walletAddress.length > 20;
  }
  
  _generateTransactionId() {
    return Math.random().toString(36).substr(2, 9);
  }
}

// Simplified payment processor
class PaymentProcessor {
  processPayment(paymentMethod) {
    return paymentMethod.process();
  }
  
  calculateTotalCost(paymentMethod) {
    const fee = paymentMethod.calculateFee();
    return paymentMethod.amount + fee;
  }
}

// Usage
const processor = new PaymentProcessor();

const creditCard = new CreditCardPayment(100, '1234567890123456', '12/25', '123');
const paypal = new PayPalPayment(100, 'user@example.com', 'password');
const bankTransfer = new BankTransferPayment(1500, '12345678', '987654321');

console.log(processor.processPayment(creditCard));
console.log(processor.processPayment(paypal));
console.log(processor.processPayment(bankTransfer));

// Easy to add new payment methods without modifying existing code
class ApplePayPayment extends PaymentMethod {
  constructor(amount, touchId) {
    super(amount);
    this._touchId = touchId;
  }
  
  process() {
    // Apple Pay specific processing
    return {
      success: true,
      transactionId: 'ap_' + Math.random().toString(36).substr(2, 9),
      fee: this.calculateFee(),
      processingTime: this.getProcessingTime()
    };
  }
  
  calculateFee() {
    return 0; // Apple Pay has no fees
  }
  
  getProcessingTime() {
    return 'instant';
  }
  
  validate() {
    return this._touchId;
  }
}
```

### Document Processing Example
```javascript
// Before - Conditional document processing
class DocumentProcessor {
  processDocument(document) {
    switch (document.type) {
      case 'pdf':
        return this._processPDF(document);
      case 'word':
        return this._processWord(document);
      case 'excel':
        return this._processExcel(document);
      case 'powerpoint':
        return this._processPowerPoint(document);
      default:
        throw new Error(`Unsupported document type: ${document.type}`);
    }
  }
  
  extractText(document) {
    switch (document.type) {
      case 'pdf':
        return this._extractTextFromPDF(document);
      case 'word':
        return this._extractTextFromWord(document);
      case 'excel':
        return this._extractTextFromExcel(document);
      case 'powerpoint':
        return this._extractTextFromPowerPoint(document);
      default:
        throw new Error(`Cannot extract text from: ${document.type}`);
    }
  }
  
  generateThumbnail(document) {
    switch (document.type) {
      case 'pdf':
        return this._generatePDFThumbnail(document);
      case 'word':
        return this._generateWordThumbnail(document);
      case 'excel':
        return this._generateExcelThumbnail(document);
      case 'powerpoint':
        return this._generatePowerPointThumbnail(document);
      default:
        throw new Error(`Cannot generate thumbnail for: ${document.type}`);
    }
  }
  
  // Individual processing methods...
  _processPDF(document) { /* PDF processing */ }
  _processWord(document) { /* Word processing */ }
  _processExcel(document) { /* Excel processing */ }
  _processPowerPoint(document) { /* PowerPoint processing */ }
  
  _extractTextFromPDF(document) { /* PDF text extraction */ }
  _extractTextFromWord(document) { /* Word text extraction */ }
  _extractTextFromExcel(document) { /* Excel text extraction */ }
  _extractTextFromPowerPoint(document) { /* PowerPoint text extraction */ }
  
  _generatePDFThumbnail(document) { /* PDF thumbnail */ }
  _generateWordThumbnail(document) { /* Word thumbnail */ }
  _generateExcelThumbnail(document) { /* Excel thumbnail */ }
  _generatePowerPointThumbnail(document) { /* PowerPoint thumbnail */ }
}

// After - Polymorphic document processing
class Document {
  constructor(filename, content) {
    this._filename = filename;
    this._content = content;
    this._processedAt = null;
  }
  
  get filename() { return this._filename; }
  get content() { return this._content; }
  get processedAt() { return this._processedAt; }
  
  // Abstract methods
  process() {
    throw new Error('Subclasses must implement process');
  }
  
  extractText() {
    throw new Error('Subclasses must implement extractText');
  }
  
  generateThumbnail() {
    throw new Error('Subclasses must implement generateThumbnail');
  }
  
  getMetadata() {
    throw new Error('Subclasses must implement getMetadata');
  }
  
  // Common functionality
  markAsProcessed() {
    this._processedAt = new Date();
  }
}

class PDFDocument extends Document {
  constructor(filename, content) {
    super(filename, content);
    this._pageCount = 0;
  }
  
  process() {
    // PDF-specific processing
    this._pageCount = this._calculatePageCount();
    this.markAsProcessed();
    return {
      type: 'pdf',
      filename: this._filename,
      pageCount: this._pageCount,
      textLength: this.extractText().length
    };
  }
  
  extractText() {
    // PDF text extraction logic
    return this._content.replace(/<[^>]*>/g, ''); // Simplified
  }
  
  generateThumbnail() {
    // PDF thumbnail generation
    return {
      type: 'image/png',
      data: this._renderFirstPage(),
      width: 200,
      height: 260
    };
  }
  
  getMetadata() {
    return {
      type: 'pdf',
      pageCount: this._pageCount,
      size: this._content.length,
      created: this._processedAt
    };
  }
  
  _calculatePageCount() {
    // Simplified page counting
    return Math.ceil(this._content.length / 3000);
  }
  
  _renderFirstPage() {
    // Simplified rendering
    return 'base64_thumbnail_data';
  }
}

class WordDocument extends Document {
  constructor(filename, content) {
    super(filename, content);
    this._wordCount = 0;
  }
  
  process() {
    // Word-specific processing
    this._wordCount = this._calculateWordCount();
    this.markAsProcessed();
    return {
      type: 'word',
      filename: this._filename,
      wordCount: this._wordCount,
      textLength: this.extractText().length
    };
  }
  
  extractText() {
    // Word text extraction logic
    return this._content.replace(/\r\n/g, ' ').trim();
  }
  
  generateThumbnail() {
    // Word thumbnail generation
    return {
      type: 'image/png',
      data: this._renderPreview(),
      width: 200,
      height: 260
    };
  }
  
  getMetadata() {
    return {
      type: 'word',
      wordCount: this._wordCount,
      size: this._content.length,
      created: this._processedAt
    };
  }
  
  _calculateWordCount() {
    return this.extractText().split(/\s+/).length;
  }
  
  _renderPreview() {
    return 'word_preview_data';
  }
}

class ExcelDocument extends Document {
  constructor(filename, content) {
    super(filename, content);
    this._sheetCount = 0;
    this._cellCount = 0;
  }
  
  process() {
    // Excel-specific processing
    this._analyzeSpreadsheet();
    this.markAsProcessed();
    return {
      type: 'excel',
      filename: this._filename,
      sheetCount: this._sheetCount,
      cellCount: this._cellCount
    };
  }
  
  extractText() {
    // Excel text extraction logic
    return this._content.replace(/,/g, ' ').replace(/\n/g, ' ');
  }
  
  generateThumbnail() {
    // Excel thumbnail generation
    return {
      type: 'image/png',
      data: this._renderSpreadsheetPreview(),
      width: 200,
      height: 260
    };
  }
  
  getMetadata() {
    return {
      type: 'excel',
      sheetCount: this._sheetCount,
      cellCount: this._cellCount,
      size: this._content.length,
      created: this._processedAt
    };
  }
  
  _analyzeSpreadsheet() {
    // Simplified analysis
    this._sheetCount = 1;
    this._cellCount = this._content.split(',').length;
  }
  
  _renderSpreadsheetPreview() {
    return 'excel_preview_data';
  }
}

// Simplified processor
class DocumentProcessor {
  processDocument(document) {
    return document.process();
  }
  
  extractAllText(documents) {
    return documents.map(doc => ({
      filename: doc.filename,
      text: doc.extractText()
    }));
  }
  
  generateAllThumbnails(documents) {
    return documents.map(doc => ({
      filename: doc.filename,
      thumbnail: doc.generateThumbnail()
    }));
  }
}

// Usage
const processor = new DocumentProcessor();

const documents = [
  new PDFDocument('report.pdf', 'PDF content here...'),
  new WordDocument('letter.docx', 'Word content here...'),
  new ExcelDocument('data.xlsx', 'cell1,cell2,cell3\nvalue1,value2,value3')
];

documents.forEach(doc => {
  console.log(processor.processDocument(doc));
});
```

## Mechanics

1. **Identify conditional logic patterns**
   - Look for switch statements or if-else chains based on type
   - Find repeated conditional logic across methods
   - Check for type codes or enum-based decisions

2. **Create inheritance hierarchy**
   - Define a base class with abstract methods
   - Create subclasses for each type/case
   - Move type-specific logic to appropriate subclasses

3. **Replace conditionals with polymorphic calls**
   - Remove switch/if-else statements
   - Let objects handle their own behavior
   - Use method overriding instead of conditional logic

4. **Update client code**
   - Change object creation to use specific subclasses
   - Remove type checking logic
   - Use polymorphic method calls

5. **Test thoroughly**
   - Ensure all behaviors are preserved
   - Verify new types can be added without modifying existing code
   - Check that polymorphism works correctly

## When to Use

- **Type-based conditionals**: Switch statements or if-else chains based on object type
- **Repeated patterns**: Same conditional logic appears in multiple places
- **Extensibility needs**: Frequently adding new types or behaviors
- **Complex business rules**: Different types have significantly different behaviors
- **Open/Closed Principle**: Want to extend behavior without modifying existing code

## Trade-offs

### Benefits
- **Extensibility**: Easy to add new types without modifying existing code
- **Encapsulation**: Behavior is coupled with data
- **Maintainability**: Changes to type behavior are localized
- **Polymorphism**: Uniform interface for different types
- **Open/Closed Principle**: Open for extension, closed for modification

### Drawbacks
- **Increased complexity**: More classes and inheritance relationships
- **Indirection**: Behavior is spread across multiple classes
- **Over-engineering**: May be overkill for simple conditionals
- **Learning curve**: Requires understanding of inheritance and polymorphism

## Design Patterns and Alternatives

### Strategy Pattern
```javascript
// Use strategy pattern for algorithms
class SortingContext {
  constructor(strategy) {
    this._strategy = strategy;
  }
  
  sort(data) {
    return this._strategy.sort(data);
  }
}

class QuickSort {
  sort(data) {
    // Quick sort implementation
  }
}

class MergeSort {
  sort(data) {
    // Merge sort implementation
  }
}
```

### State Pattern
```javascript
// Use state pattern for state-dependent behavior
class TrafficLight {
  constructor() {
    this._state = new RedState();
  }
  
  change() {
    this._state = this._state.next();
  }
  
  getColor() {
    return this._state.getColor();
  }
}

class RedState {
  getColor() { return 'red'; }
  next() { return new GreenState(); }
}

class GreenState {
  getColor() { return 'green'; }
  next() { return new YellowState(); }
}
```

### Factory Pattern
```javascript
// Use factory pattern for object creation
class ShapeFactory {
  static createShape(type, ...args) {
    switch (type) {
      case 'circle':
        return new Circle(...args);
      case 'square':
        return new Square(...args);
      default:
        throw new Error(`Unknown shape: ${type}`);
    }
  }
}
```

## Related Refactorings

- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - Create the subclass structure
- [Extract Class](extract-class.md) - Create strategy classes
- [Move Method](move-method.md) - Move type-specific behavior to subclasses
- [Replace Parameter with Query](replace-parameter-with-query.md) - Remove type parameters
- [Introduce Polymorphism](introduce-parameter-object.md) - Alternative approach to conditional logic