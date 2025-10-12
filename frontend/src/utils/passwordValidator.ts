/**
 * Password validation utilities for the frontend
 */

export interface PasswordRequirement {
  text: string;
  isValid: boolean;
}

export interface PasswordValidationResult {
  isValid: boolean;
  requirements: PasswordRequirement[];
  score: number; // 0-100 strength score
}

export class PasswordValidator {
  private static readonly MIN_LENGTH = 8;
  private static readonly SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:,.<>?";

  private static readonly COMMON_PASSWORDS = new Set([
    "password",
    "123456",
    "password123",
    "admin",
    "qwerty",
    "letmein",
    "welcome",
    "monkey",
    "1234567890",
    "abc123",
    "123456789",
    "password1",
    "iloveyou",
    "123123",
    "admin123",
    "qwerty123",
    "password12",
    "welcome123",
    "master",
    "hello",
    "login",
    "guest",
    "test",
    "user",
    "root",
    "toor",
  ]);

  /**
   * Validate password and return detailed results
   */
  static validatePassword(password: string): PasswordValidationResult {
    const requirements: PasswordRequirement[] = [
      {
        text: `At least ${this.MIN_LENGTH} characters long`,
        isValid: password.length >= this.MIN_LENGTH,
      },
      {
        text: "At least one uppercase letter (A-Z)",
        isValid: /[A-Z]/.test(password),
      },
      {
        text: "At least one lowercase letter (a-z)",
        isValid: /[a-z]/.test(password),
      },
      {
        text: "At least one digit (0-9)",
        isValid: /\d/.test(password),
      },
      {
        text: `At least one special character (${this.SPECIAL_CHARACTERS})`,
        isValid: new RegExp(
          `[${this.escapeRegExp(this.SPECIAL_CHARACTERS)}]`
        ).test(password),
      },
      {
        text: "Not a common password",
        isValid: !this.COMMON_PASSWORDS.has(password.toLowerCase()),
      },
      {
        text: "No more than 3 consecutive identical characters",
        isValid: !/(.)\1{3,}/.test(password),
      },
      {
        text: "No simple sequences (like '1234' or 'abcd')",
        isValid: !this.containsSimpleSequence(password),
      },
    ];

    const validCount = requirements.filter((req) => req.isValid).length;
    const isValid = validCount === requirements.length;
    const score = Math.round((validCount / requirements.length) * 100);

    return {
      isValid,
      requirements,
      score,
    };
  }

  /**
   * Get password strength level based on score
   */
  static getStrengthLevel(score: number): "weak" | "fair" | "good" | "strong" {
    if (score < 40) return "weak";
    if (score < 60) return "fair";
    if (score < 80) return "good";
    return "strong";
  }

  /**
   * Get color for password strength indicator
   */
  static getStrengthColor(score: number): string {
    if (score < 40) return "#ef4444"; // red
    if (score < 60) return "#f59e0b"; // yellow
    if (score < 80) return "#3b82f6"; // blue
    return "#10b981"; // green
  }

  private static escapeRegExp(string: string): string {
    return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  private static containsSimpleSequence(password: string): boolean {
    const passwordLower = password.toLowerCase();

    const sequences = [
      "0123456789",
      "abcdefghijklmnopqrstuvwxyz",
      "qwertyuiopasdfghjklzxcvbnm", // QWERTY keyboard layout
    ];

    for (const sequence of sequences) {
      for (let i = 0; i <= sequence.length - 4; i++) {
        const subseq = sequence.substring(i, i + 4);
        const reverseSubseq = subseq.split("").reverse().join("");

        if (
          passwordLower.includes(subseq) ||
          passwordLower.includes(reverseSubseq)
        ) {
          return true;
        }
      }
    }

    return false;
  }
}
