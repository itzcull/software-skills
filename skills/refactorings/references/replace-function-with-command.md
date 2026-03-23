---
title: "Replace Function with Command"
description: "Turn a function into a command object for more flexibility and complex operations"
category: "Organization"
tags: ["function", "command", "undo", "queuing", "logging", "parameterization"]
related: ["replace-constructor-with-factory-function", "extract-class", "parameterize-function"]
---

# Replace Function with Command

Turn a function into a command object. This provides more flexibility for complex operations, allowing for undo functionality, queuing, logging, and parameterization.

## Motivation

Functions can become limiting when you need:

- **Undo functionality**: Ability to reverse operations
- **Complex parameterization**: More sophisticated parameter handling
- **Logging and auditing**: Track when and how operations are performed
- **Queuing and scheduling**: Defer or batch operations
- **Progress tracking**: Monitor long-running operations
- **Macro recording**: Combine multiple operations
- **Validation**: Complex pre-condition checking

## Example

### Basic Example
```javascript
// Before - Simple function
function calculateShippingCost(order, shippingMethod, destination) {
  const baseRate = getBaseShippingRate(shippingMethod);
  const distance = calculateDistance(order.origin, destination);
  const weight = order.items.reduce((total, item) => total + item.weight, 0);
  
  let cost = baseRate + (distance * 0.01) + (weight * 0.05);
  
  // Apply discounts
  if (order.customer.isPremium) {
    cost *= 0.9; // 10% discount
  }
  
  if (order.total > 100) {
    cost *= 0.95; // 5% discount for large orders
  }
  
  return Math.max(cost, 5.00); // Minimum shipping cost
}

// Usage
const shippingCost = calculateShippingCost(order, 'express', customerAddress);

// After - Command object with more capabilities
class CalculateShippingCostCommand {
  constructor(order, shippingMethod, destination) {
    this._order = order;
    this._shippingMethod = shippingMethod;
    this._destination = destination;
    this._calculationSteps = [];
    this._result = null;
    this._executedAt = null;
  }
  
  execute() {
    this._executedAt = new Date();
    this._calculationSteps = [];
    
    const baseRate = this._getBaseShippingRate();
    this._addStep('Base rate', baseRate);
    
    const distance = this._calculateDistance();
    const distanceCost = distance * 0.01;
    this._addStep('Distance cost', distanceCost, { distance });
    
    const weight = this._calculateWeight();
    const weightCost = weight * 0.05;
    this._addStep('Weight cost', weightCost, { weight });
    
    let totalCost = baseRate + distanceCost + weightCost;
    this._addStep('Subtotal', totalCost);
    
    // Apply discounts
    if (this._order.customer.isPremium) {
      const discount = totalCost * 0.1;
      totalCost -= discount;
      this._addStep('Premium discount', -discount);
    }
    
    if (this._order.total > 100) {
      const discount = totalCost * 0.05;
      totalCost -= discount;
      this._addStep('Large order discount', -discount);
    }
    
    // Apply minimum
    if (totalCost < 5.00) {
      this._addStep('Minimum shipping applied', 5.00 - totalCost);
      totalCost = 5.00;
    }
    
    this._result = totalCost;
    this._addStep('Final cost', totalCost);
    
    return this._result;
  }
  
  getResult() {
    if (this._result === null) {
      throw new Error('Command has not been executed yet');
    }
    return this._result;
  }
  
  getCalculationBreakdown() {
    return {
      steps: [...this._calculationSteps],
      executedAt: this._executedAt,
      order: this._order.id,
      shippingMethod: this._shippingMethod,
      destination: this._destination
    };
  }
  
  _getBaseShippingRate() {
    const rates = {
      'standard': 5.00,
      'express': 15.00,
      'overnight': 25.00
    };
    return rates[this._shippingMethod] || rates['standard'];
  }
  
  _calculateDistance() {
    // Simplified distance calculation
    return Math.sqrt(
      Math.pow(this._order.origin.lat - this._destination.lat, 2) +
      Math.pow(this._order.origin.lng - this._destination.lng, 2)
    ) * 111; // Convert to km
  }
  
  _calculateWeight() {
    return this._order.items.reduce((total, item) => total + item.weight, 0);
  }
  
  _addStep(description, amount, metadata = {}) {
    this._calculationSteps.push({
      description,
      amount,
      metadata,
      timestamp: new Date()
    });
  }
}

// Usage with enhanced capabilities
const command = new CalculateShippingCostCommand(order, 'express', customerAddress);
const shippingCost = command.execute();

// Get detailed breakdown for auditing
const breakdown = command.getCalculationBreakdown();
console.log('Shipping calculation:', breakdown);
```

### Complex Example - File Processing Command
```javascript
// Before - Function with limited capabilities
function processFile(filePath, options = {}) {
  const content = fs.readFileSync(filePath, 'utf8');
  
  let processed = content;
  
  if (options.removeComments) {
    processed = processed.replace(/\/\*[\s\S]*?\*\//g, '');
    processed = processed.replace(/\/\/.*$/gm, '');
  }
  
  if (options.minify) {
    processed = processed.replace(/\s+/g, ' ').trim();
  }
  
  if (options.addHeader) {
    processed = `/* Processed at ${new Date().toISOString()} */\n${processed}`;
  }
  
  if (options.outputPath) {
    fs.writeFileSync(options.outputPath, processed);
  }
  
  return processed;
}

// After - Command object with undo, logging, and progress tracking
class ProcessFileCommand {
  constructor(filePath, options = {}) {
    this._filePath = filePath;
    this._options = { ...options };
    this._originalContent = null;
    this._processedContent = null;
    this._steps = [];
    this._startTime = null;
    this._endTime = null;
    this._undoData = [];
  }
  
  async execute() {
    this._startTime = Date.now();
    this._log('Starting file processing');
    
    try {
      // Read original file
      this._originalContent = await this._readFile();
      this._processedContent = this._originalContent;
      this._log('File read successfully', { size: this._originalContent.length });
      
      // Process in steps
      if (this._options.removeComments) {
        await this._removeComments();
      }
      
      if (this._options.minify) {
        await this._minify();
      }
      
      if (this._options.addHeader) {
        await this._addHeader();
      }
      
      if (this._options.outputPath) {
        await this._writeOutput();
      }
      
      this._endTime = Date.now();
      this._log('Processing completed successfully');
      
      return this._processedContent;
      
    } catch (error) {
      this._log('Processing failed', { error: error.message });
      throw error;
    }
  }
  
  async undo() {
    if (!this._options.outputPath) {
      throw new Error('Cannot undo: no output file was created');
    }
    
    this._log('Starting undo operation');
    
    try {
      if (this._undoData.length > 0) {
        const undoInfo = this._undoData[this._undoData.length - 1];
        if (undoInfo.type === 'file_write' && undoInfo.backupPath) {
          // Restore from backup
          const fs = require('fs').promises;
          await fs.copyFile(undoInfo.backupPath, this._options.outputPath);
          await fs.unlink(undoInfo.backupPath);
          this._log('File restored from backup');
        } else if (undoInfo.type === 'file_create') {
          // Delete created file
          const fs = require('fs').promises;
          await fs.unlink(this._options.outputPath);
          this._log('Created file deleted');
        }
      }
      
      this._log('Undo completed successfully');
      
    } catch (error) {
      this._log('Undo failed', { error: error.message });
      throw error;
    }
  }
  
  getProgress() {
    const totalSteps = this._getTotalSteps();
    const completedSteps = this._steps.filter(step => step.completed).length;
    
    return {
      completed: completedSteps,
      total: totalSteps,
      percentage: Math.round((completedSteps / totalSteps) * 100),
      currentStep: this._getCurrentStep(),
      elapsedTime: this._startTime ? Date.now() - this._startTime : 0
    };
  }
  
  getExecutionLog() {
    return {
      filePath: this._filePath,
      options: this._options,
      steps: [...this._steps],
      startTime: this._startTime,
      endTime: this._endTime,
      duration: this._endTime ? this._endTime - this._startTime : null,
      originalSize: this._originalContent ? this._originalContent.length : null,
      processedSize: this._processedContent ? this._processedContent.length : null
    };
  }
  
  async _readFile() {
    const fs = require('fs').promises;
    return await fs.readFile(this._filePath, 'utf8');
  }
  
  async _removeComments() {
    this._log('Removing comments');
    const before = this._processedContent;
    
    // Remove block comments
    this._processedContent = this._processedContent.replace(/\/\*[\s\S]*?\*\//g, '');
    // Remove line comments
    this._processedContent = this._processedContent.replace(/\/\/.*$/gm, '');
    
    const removed = before.length - this._processedContent.length;
    this._log('Comments removed', { charactersRemoved: removed });
  }
  
  async _minify() {
    this._log('Minifying content');
    const before = this._processedContent;
    
    this._processedContent = this._processedContent
      .replace(/\s+/g, ' ')
      .trim();
    
    const saved = before.length - this._processedContent.length;
    this._log('Content minified', { charactersSaved: saved });
  }
  
  async _addHeader() {
    this._log('Adding header');
    const header = `/* Processed at ${new Date().toISOString()} */\n`;
    this._processedContent = header + this._processedContent;
    this._log('Header added', { headerLength: header.length });
  }
  
  async _writeOutput() {
    this._log('Writing output file');
    const fs = require('fs').promises;
    
    // Check if output file exists for undo functionality
    try {
      await fs.access(this._options.outputPath);
      // File exists, create backup
      const backupPath = `${this._options.outputPath}.backup.${Date.now()}`;
      await fs.copyFile(this._options.outputPath, backupPath);
      this._undoData.push({ type: 'file_write', backupPath });
      this._log('Backup created', { backupPath });
    } catch {
      // File doesn't exist, mark for deletion on undo
      this._undoData.push({ type: 'file_create' });
    }
    
    await fs.writeFile(this._options.outputPath, this._processedContent, 'utf8');
    this._log('Output file written', { path: this._options.outputPath });
  }
  
  _log(message, metadata = {}) {
    this._steps.push({
      message,
      metadata,
      timestamp: new Date(),
      completed: true
    });
  }
  
  _getTotalSteps() {
    let steps = 1; // Read file
    if (this._options.removeComments) steps++;
    if (this._options.minify) steps++;
    if (this._options.addHeader) steps++;
    if (this._options.outputPath) steps++;
    return steps;
  }
  
  _getCurrentStep() {
    if (!this._steps.length) return 'Initializing';
    return this._steps[this._steps.length - 1].message;
  }
}

// Command manager for queuing and batch operations
class CommandQueue {
  constructor() {
    this._commands = [];
    this._history = [];
    this._isProcessing = false;
  }
  
  addCommand(command) {
    this._commands.push(command);
  }
  
  async executeAll() {
    if (this._isProcessing) {
      throw new Error('Commands are already being processed');
    }
    
    this._isProcessing = true;
    const results = [];
    
    try {
      for (const command of this._commands) {
        const result = await command.execute();
        results.push(result);
        this._history.push(command);
      }
      
      this._commands = [];
      return results;
      
    } finally {
      this._isProcessing = false;
    }
  }
  
  async undoLast() {
    if (this._history.length === 0) {
      throw new Error('No commands to undo');
    }
    
    const lastCommand = this._history.pop();
    if (typeof lastCommand.undo === 'function') {
      await lastCommand.undo();
    }
  }
  
  getProgress() {
    if (!this._isProcessing) {
      return { completed: 0, total: this._commands.length, percentage: 0 };
    }
    
    const totalCommands = this._commands.length + this._history.length;
    const completedCommands = this._history.length;
    
    return {
      completed: completedCommands,
      total: totalCommands,
      percentage: Math.round((completedCommands / totalCommands) * 100)
    };
  }
}

// Usage with enhanced capabilities
async function processMultipleFiles() {
  const queue = new CommandQueue();
  
  // Add multiple file processing commands
  queue.addCommand(new ProcessFileCommand('file1.js', {
    removeComments: true,
    minify: true,
    outputPath: 'dist/file1.min.js'
  }));
  
  queue.addCommand(new ProcessFileCommand('file2.js', {
    removeComments: true,
    addHeader: true,
    outputPath: 'dist/file2.processed.js'
  }));
  
  try {
    const results = await queue.executeAll();
    console.log('All files processed successfully');
    
  } catch (error) {
    console.error('Processing failed:', error.message);
    
    // Undo the last successful command
    try {
      await queue.undoLast();
      console.log('Last operation undone');
    } catch (undoError) {
      console.error('Undo failed:', undoError.message);
    }
  }
}
```

### Macro Command Example
```javascript
// Composite command for complex operations
class MacroCommand {
  constructor(name, commands = []) {
    this._name = name;
    this._commands = commands;
    this._executedCommands = [];
  }
  
  addCommand(command) {
    this._commands.push(command);
  }
  
  async execute() {
    this._executedCommands = [];
    
    try {
      for (const command of this._commands) {
        await command.execute();
        this._executedCommands.push(command);
      }
      
    } catch (error) {
      // If any command fails, undo all executed commands
      await this._undoExecutedCommands();
      throw error;
    }
  }
  
  async undo() {
    await this._undoExecutedCommands();
  }
  
  async _undoExecutedCommands() {
    // Undo in reverse order
    for (let i = this._executedCommands.length - 1; i >= 0; i--) {
      const command = this._executedCommands[i];
      if (typeof command.undo === 'function') {
        await command.undo();
      }
    }
    this._executedCommands = [];
  }
}

// Usage: Build deployment pipeline
const deploymentPipeline = new MacroCommand('Deploy Application', [
  new ProcessFileCommand('src/app.js', { minify: true, outputPath: 'dist/app.min.js' }),
  new ProcessFileCommand('src/styles.css', { minify: true, outputPath: 'dist/styles.min.css' }),
  new CreateArchiveCommand('dist/', 'deploy.zip'),
  new UploadCommand('deploy.zip', 'production-server'),
  new RestartServiceCommand('my-app-service')
]);

try {
  await deploymentPipeline.execute();
  console.log('Deployment successful');
} catch (error) {
  console.error('Deployment failed, rolling back:', error.message);
}
```

## Mechanics

1. **Identify complex functions**
   - Look for functions that need undo capability
   - Find functions with complex parameter validation
   - Check for functions that would benefit from logging or progress tracking

2. **Create command class**
   - Define a class that encapsulates the operation
   - Move function parameters to constructor
   - Move function body to execute() method

3. **Add command capabilities**
   - Implement undo() method if needed
   - Add logging and progress tracking
   - Provide access to execution metadata

4. **Update client code**
   - Replace function calls with command creation and execution
   - Add error handling for command execution
   - Use command features like undo and logging

5. **Consider command patterns**
   - Implement command queue for batch operations
   - Create macro commands for complex workflows
   - Add command history for undo/redo functionality

6. **Test thoroughly**
   - Verify that command execution produces correct results
   - Test undo functionality if implemented
   - Check that logging and progress tracking work correctly

## When to Use

- **Undo/redo needed**: Operations that users might want to reverse
- **Complex operations**: Functions with many steps or long execution times
- **Batch processing**: Need to queue or schedule operations
- **Audit requirements**: Operations that need detailed logging
- **Progress tracking**: Long-running operations that need progress updates
- **Macro functionality**: Combining multiple operations into workflows
- **Transactional behavior**: Operations that need all-or-nothing execution

## Trade-offs

### Benefits
- **Undo functionality**: Can reverse operations
- **Logging and auditing**: Track operation execution
- **Progress tracking**: Monitor long-running operations
- **Queuing**: Batch and schedule operations
- **Composability**: Combine commands into macros
- **Testability**: Easier to test complex operations

### Drawbacks
- **Increased complexity**: More code than simple functions
- **Memory overhead**: Command objects take more memory
- **Indirection**: Less direct than function calls
- **Learning curve**: Team needs to understand command pattern

## Design Patterns

### Command Interface
```javascript
class Command {
  execute() {
    throw new Error('Subclasses must implement execute');
  }
  
  undo() {
    throw new Error('Subclasses must implement undo');
  }
  
  canUndo() {
    return false;
  }
}
```

### Receiver Pattern
```javascript
class TextEditor {
  constructor() {
    this._content = '';
  }
  
  insertText(text, position) {
    this._content = this._content.slice(0, position) + text + this._content.slice(position);
  }
  
  deleteText(start, length) {
    return this._content.slice(start, start + length);
  }
}

class InsertTextCommand extends Command {
  constructor(editor, text, position) {
    super();
    this._editor = editor;
    this._text = text;
    this._position = position;
  }
  
  execute() {
    this._editor.insertText(this._text, this._position);
  }
  
  undo() {
    this._editor.deleteText(this._position, this._text.length);
  }
}
```

### Invoker Pattern
```javascript
class CommandManager {
  constructor() {
    this._history = [];
    this._currentIndex = -1;
  }
  
  executeCommand(command) {
    command.execute();
    
    // Remove any commands after current index
    this._history = this._history.slice(0, this._currentIndex + 1);
    
    // Add new command
    this._history.push(command);
    this._currentIndex++;
  }
  
  undo() {
    if (this._currentIndex >= 0) {
      const command = this._history[this._currentIndex];
      if (command.canUndo()) {
        command.undo();
        this._currentIndex--;
      }
    }
  }
  
  redo() {
    if (this._currentIndex < this._history.length - 1) {
      this._currentIndex++;
      const command = this._history[this._currentIndex];
      command.execute();
    }
  }
}
```

## Related Refactorings

- [Extract Function](extract-function.md) - Break down command logic
- [Introduce Parameter Object](introduce-parameter-object.md) - Simplify command parameters
- [Replace Parameter with Query](replace-parameter-with-query.md) - Reduce command parameters
- [Move Method](move-method.md) - Move command logic to appropriate classes
- [Extract Class](extract-class.md) - Create command receivers