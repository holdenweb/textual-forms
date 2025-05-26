from textual.validation import Validator, ValidationResult

class EvenInteger(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            value = int(value)
        except ValueError:
            return self.success()  # Handled by other validators
        if value % 2:
            return self.failure("Not an even number")
        else:
            return self.success()

class Palindromic(Validator):
    def validate(self, value: str) -> ValidationResult:
        if value == value[::-1]:
            return self.success()
        else:
            return self.failure("Not palindromic")


