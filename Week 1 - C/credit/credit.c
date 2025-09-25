#include <cs50.h>
#include <math.h>
#include <stdio.h>

bool VISA1(long n);
bool AMEX(long n);
bool MASTERCARD(long n);
bool VISA(long n);
int length(long n);
int multiplySum(int last_digit);

int digits(long card_number);

int main(void)
{

    long credit_card_number = get_long("Enter ur credit card number : ");
    long length_of_number = length(credit_card_number);


    int sum_of_digit1 = digits(credit_card_number);

    bool amex = AMEX(credit_card_number);
    bool mastercard = MASTERCARD(credit_card_number);
    bool visa = VISA(credit_card_number);
    bool visa1 = VISA1(credit_card_number);


    if (sum_of_digit1 % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    else if (amex == true)
    {
        printf("AMEX\n");
    }
    else if (mastercard == true)
    {
        printf("MASTERCARD\n");
    }
    else if (visa == true)
    {
        printf("VISA\n");
    }
    else if (visa1 == true)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }
}

int length(long n)
{
    int count = 0;
    while (n > 0)
    {
        count++;
        n = n / 10;
    }
    return (count);
}

int digits(long card_number)
{
    int sum = 0;
    bool isAlternateDigit = false;
    while (card_number > 0)
    {
        if (isAlternateDigit == true)
        {
            int last_digit = card_number % 10;
            int product = multiplySum(last_digit);

            sum = sum + product;
        }
        else
        {
            int last_digit = card_number % 10;
            sum = sum + last_digit;
        }
        isAlternateDigit = !isAlternateDigit;
        card_number = card_number / 10;
    }
    return sum;
}

int multiplySum(int last_digit)
{
    int multiply = last_digit * 2;
    int sum = 0;

    while (multiply > 0)
    {
        int last_digit_multiply = multiply % 10;
        sum = sum + last_digit_multiply;
        multiply /= 10;
    }
    return sum;
}

bool AMEX(long n)
{
    int first_digit = n / pow(10, 13);
    int x = length(n);
    if (((first_digit == 34) || (first_digit == 37)) && (x == 15))
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool MASTERCARD(long n)
{
    int first_digit = n / pow(10, 14);
    int x = length(n);
    if (((first_digit == 51) || (first_digit == 52) || (first_digit == 53) || (first_digit == 54) ||
         (first_digit == 55)) &&
        (x == 16))
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool VISA(long n)
{
    int first_digit = n / pow(10, 12);
    int x = length(n);
    if ((first_digit == 4) && (x == 13))
    {
        return true;
    }
    else
    {
        return false;
    }

}

bool VISA1(long n)
{
    int first_digit = n / pow(10, 15);
    int x = length(n);
    if ((first_digit == 4) && (x == 16))
    {
        return true;
    }
    else
    {
        return false;
    }
}
