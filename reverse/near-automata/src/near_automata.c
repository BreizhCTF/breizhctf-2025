#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include "biguint128.h"

#define N 128

void str_to_hex(char* input, char* hex_representation) {
        for (int i = 0; i < strlen(input); i++) {
                sprintf(hex_representation + i*2, "%02x", input[i]);
        }
}

int checkFlag(BigUInt128* second_state, BigUInt128* state) {
        UInt flag_array[4] = {1560134675, 1434780471, 3796314293, 3180861283};
        UInt second_array[4] = {4109998979 ,1397427179 , 589225631, 2626754790};
        BigUInt128 flag = biguint128_ctor_standard(flag_array);
        BigUInt128 second_flag = biguint128_ctor_standard(second_array);
        if (biguint128_eq(state, &flag) && biguint128_eq(second_state, &second_flag)) {
                printf("Good job !\nYour input is the flag\n");
                exit(0);
        } else {
                printf("Try again !\n");
                exit(1);
        }
}

BigUInt128 B(int x) {
        BigUInt128 one = biguint128_ctor_unit();
        return biguint128_shl(&one, x);
}


unsigned int B2(BigUInt128 x) {
        return 1 << x.dat[0];
}


void evolve(BigUInt128 state1 ,BigUInt128 state2, unsigned int rule)
{
        unsigned int counter = 0;
        unsigned int i;
        BigUInt128 st1 = state2;
        BigUInt128 st2;
        BigUInt128 state = state1;

        do {
                st2 = st1;
                st1 = state;

                state = biguint128_ctor_default();

                for (i = 0; i < N; i++) {
                        BigUInt128 shr = biguint128_shr(&st1, (i-1));
                        BigUInt128 shl = biguint128_shl(&st1, (N+1-i));

                        BigUInt128 or = biguint128_or(&shr, &shl);
                        BigUInt128 seven = biguint128_value_of_uint(7);

                        unsigned int val = B2(biguint128_and(&seven, &or));
                        unsigned int new_value = rule & val;

                        if (new_value != 0) {
                                BigUInt128 val = B(i);
                                state = biguint128_or(&state, &val);
                        }
                }
                state = biguint128_xor(&state, &st2);

                counter++;
        } while (counter < 1338);
        checkFlag(&state, &st1);
}


int main(int argc, char **argv)
{
        printf("|-----------------------------------------------------|\n");
        printf("|                 Near Automata v3.5.7                |\n");
        printf("|-----------------------------------------------------|\n");
        //char* first_flag = "425a484354467b49745f346c57347935";   // BZHCTF{It_4lW4y5
        //char* second_flag = "5f336e64355f6c316b335f746831357d"; // _3nd5_l1k3_th15}

        if (argc != 3) {
                return 1;
        }

        // Get the lengths of the two arguments
        size_t len1 = strlen(argv[1]);
        size_t len2 = strlen(argv[2]);

        // Check if both lengths are exactly 32 characters
        if (len1 != 16) {
                return 1;
        }

        if (len2 != 16) {
                return 1;
        }

        char hex_string_0[33];
        char hex_string_1[33];

        str_to_hex(argv[1], hex_string_0);
        str_to_hex(argv[2], hex_string_1);

        evolve(biguint128_ctor_hexcstream(hex_string_0, strlen(hex_string_0)), biguint128_ctor_hexcstream(hex_string_1, strlen(hex_string_1)), 214);

        return 0;
}