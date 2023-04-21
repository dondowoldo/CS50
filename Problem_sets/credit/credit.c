#include <cs50.h>
#include <stdio.h>

// IF ANYONE IS READING THIS - APOLOGIES FOR QUITE MESSY COMMENTS. I HAD THEM NEATLY STORED ON THE RIGHT SIDE
// OF MY CODE BUT STYLE50 WAS THROWING OUT ERRORS WHILE THERE WAS NOTHING TO CORRECT
// AND I DIDN'T WANT TO LOSE POINTS IF IT WAS GRADED BY A COMPUTER. THANK YOU.

int main(void)
{
    long card_number_original, card_number_visa, card_number_master, card_number_amex, card_reversed = 0, temp;
    int number_counter, total_checksum;
    bool isVisa, isMaster, isAmex;

    card_number_original = get_long("Enter your card number: ");

    // CHECKSUM
    long check_original = card_number_original;
    long check_eliminated = check_original / 10;
    int multiplied_numbers = 0;
    int twodigitsum = 0;
    int num_not_multiplied = 0;
    while (check_eliminated != 0)
    {
        int digitselection = check_eliminated % 10;
        digitselection = digitselection * 2;
        if (digitselection > 9)
        {
            int digitsplit = digitselection % 10;
            digitselection = digitselection / 10;
            twodigitsum = twodigitsum + digitselection + digitsplit;
            digitselection = 0;
        }
        check_eliminated = check_eliminated / 100;
        multiplied_numbers = multiplied_numbers + digitselection;
    }
    multiplied_numbers = multiplied_numbers + twodigitsum;

    // similar process as above for the second part of the Luhn's Algorythm starting with
    // the last digit we previously eliminated, storing it's value and adding it on top of each
    // value stored from a previous cycle
    while (check_original != 0)
    {
        int digitselection = check_original % 10;
        num_not_multiplied = num_not_multiplied + digitselection;
        check_original = check_original / 100;
    }
    // firstly adding values together from the multiplying process and simple adding process
    // and then checking if the latter number = 0 implying a legit card
    total_checksum = multiplied_numbers + num_not_multiplied;
    total_checksum = total_checksum % 10;

    // VISA CHECK
    card_number_visa = card_number_original;
    number_counter = 0;

    // a loop that finds out how many digits does the card have by using a counter for each cycle
    // card_reversed reverse the entire card number in order to be able to capture the formerly first digit
    // (now last digit) to identify a VISA card
    while (card_number_visa != 0)
    {
        temp = card_number_visa % 10;
        card_reversed = card_reversed * 10 + temp;
        card_number_visa = card_number_visa / 10;
        number_counter++;
    }
    // if the amount of digits used by VISA fits the interval and checksum was successful,
    // program identifies card number as a VISA card
    if ((number_counter >= 13 && number_counter <= 16) && total_checksum == 0)
    {
        int visa_identifier = card_reversed % 10;
        if (visa_identifier == 4)
        {
            isVisa = true;
        }
        else
        {
            isVisa = false;
        }
    }
    else
    {
        isVisa = false;
    }
    // MASTER CHECK
    // Similar as above only this time the number of digits used is static
    // therefore we can simply divide by 100000000000000 to capture the first two digits
    card_number_master = card_number_original;
    number_counter = 0;
    int master_identifier = card_number_master / 100000000000000;

    while (card_number_master != 0)
    {
        card_number_master = card_number_master / 10;
        number_counter++;
    }

    // Identifies if the first two digits of a card entered by user
    // fit a criteria, if checksum was processed sucessfuly and if the total amount of digits fits MASTERCARD
    if (number_counter == 16 && total_checksum == 0)
    {
        switch (master_identifier)
        {
            case 51:
                isMaster = true;
                break;
            case 52:
                isMaster = true;
                break;
            case 53:
                isMaster = true;
                break;
            case 54:
                isMaster = true;
                break;
            case 55:
                isMaster = true;
                break;
            default:
                isMaster = false;
        }
    }
    else
    {
        isMaster = false;
    }

    // AMEX CHECK
    card_number_amex = card_number_original;                                                // Same process as MASTERCARD
    number_counter = 0;
    int amex_identifier = card_number_amex / 10000000000000;
    while (card_number_amex != 0)
    {
        card_number_amex = card_number_amex / 10;
        number_counter++;
    }
    if (number_counter == 15 && total_checksum == 0)
        switch (amex_identifier)
        {
            case 34:
                isAmex = true;
                break;
            case 37:
                isAmex = true;
                break;
        }

    else
    {
        isAmex = false;
    }

    if (isVisa == true)
    {
        printf("VISA\n");
    }
    else if (isMaster == true)
    {
        printf("MASTERCARD\n");
    }
    else if (isAmex == true)
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
    }

}