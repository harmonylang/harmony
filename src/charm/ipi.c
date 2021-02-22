#include <inttypes.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#define DIGIT_WIDTH 8           // # bits
typedef uint8_t udigit_t;
typedef uint16_t udigit2_t;
typedef int8_t sdigit_t;
typedef int16_t sdigit2_t;

// an infinite precision integer is represented as an array of digit_t's,
// the least significant first.  [TODO The format is 2's complement]
typedef struct ipi {
    udigit_t *digits;
    int size, sign;
} ipi_t;

char *ipi_to_string(ipi_t *ipi, int base);

void ipi_dump(ipi_t *ipi){
    printf("[%d %d:", ipi->size, ipi->sign);
    for (int i = 0; i < ipi->size; i++) {
        printf(" %d", ipi->digits[i]);
    }
    printf("]");
}

// copy but leave off shift least significant digits
void ipi_copy(ipi_t *ipi, ipi_t *x, int shift){
    int size = (x->size - shift) * sizeof(udigit_t);
    ipi->digits = malloc(size);
    memcpy(ipi->digits, &x->digits[shift], size);
    ipi->size = x->size - shift;
    ipi->sign = x->sign;        // TODO shift?
}

void ipi_trim(ipi_t *x){
    while (x->size > 0 && x->digits[x->size - 1] == 0) {
        x->size--;
    }
    x->digits = realloc(x->digits, x->size * sizeof(udigit_t));
}

void ipi_release(ipi_t *ipi){
    free(ipi->digits);
}

void ipi_from_int(ipi_t *ipi, int64_t x){
    if (x < 0) {
        ipi->sign = -1;
        x = -x;
    }
    else {
        ipi->sign = 1;
    }
    ipi->digits = malloc(64 / DIGIT_WIDTH);
    int k = 0;
    while (x != 0) {
        assert(k < 64 / DIGIT_WIDTH);
        ipi->digits[k] = x;
        x >>= DIGIT_WIDTH;
        k++;
    }
    ipi->size = k;
}

// compare x and y, non-destructively
int ipi_cmp(ipi_t *x, ipi_t *y){
    if (x->size != y->size) {
        return x->size - y->size;
    }
    for (int i = x->size - 1; i >= 0; i--) {
        if (x->digits[i] != y->digits[i]) {
            return x->digits[i] < y->digits[i] ? -1 : 1;
        }
    }
    return 0;
}

// z = x + y
void ipi_uadd(ipi_t *z, ipi_t *x, ipi_t *y){
    int carry = 0, max = x->size < y->size ? y->size : x->size;
    ipi_from_int(z, 0);
    for (int i = 0; (i < max) || (carry > 0); i++) {
        z->size++;
        z->digits = realloc(z->digits, z->size * sizeof(udigit_t));
        udigit2_t next = (i < x->size ? x->digits[i] : 0) +
                            (i < y->size ? y->digits[i] : 0) + carry;
        z->digits[i] = (udigit_t) next;
        carry = next >> DIGIT_WIDTH;
    }
}

// z = x - y (x >= y)
void ipi_usub(ipi_t *z, ipi_t *x, ipi_t *y){
    int carry = 0, max = x->size < y->size ? y->size : x->size;
    ipi_from_int(z, 0);
    for (int i = 0; (i < max) || (carry > 0); i++) {
		assert(i < x->size);
        sdigit2_t next = (sdigit2_t) x->digits[i] -
                            (carry + ((i < y->size) ? y->digits[i] : 0));
        z->size++;
        z->digits = realloc(z->digits, z->size * sizeof(udigit_t));
        if (next < 0) {
            carry = 1;
            z->digits[i] = ((udigit2_t) 1 << DIGIT_WIDTH) + next;
        }
        else {
            carry = 0;
            z->digits[i] = next;
        }
    }
    ipi_trim(z);
}

void ipi_add(ipi_t *z, ipi_t *x, ipi_t *y){
	printf("A %d %d\n", x->sign, y->sign);
	if (x->sign == y->sign) {
		ipi_uadd(z, x, y);
		z->sign = x->sign;
	}
	else {
		int cmp = ipi_cmp(x, y);
		if (cmp < 0) {
			ipi_usub(z, y, x);
			z->sign = y->sign;
		}
		else {
			ipi_usub(z, x, y);
			z->sign = x->sign;
		}
	}
}

void ipi_sub(ipi_t *z, ipi_t *x, ipi_t *y){
	if (x->sign != y->sign) {
		ipi_uadd(z, x, y);
		z->sign = x->sign;
	}
	else {
		int cmp = ipi_cmp(x, y);
		if (cmp < 0) {
			ipi_usub(z, y, x);
			z->sign = -x->sign;
		}
		else {
			ipi_usub(z, x, y);
			z->sign = -y->sign;
		}
	}
}

// x *= y
void ipi_mul_short(ipi_t *x, udigit_t y){
    udigit_t carry = 0;
    for (int i = 0; (i < x->size) || (carry > 0); i++) {
        if (i == x->size) {
            x->digits = realloc(x->digits, (x->size + 1) * sizeof(udigit_t));
            x->digits[x->size++] = 0;
        }
        udigit2_t next = carry + (udigit2_t) x->digits[i] * y;
        x->digits[i] = next;
        carry = next >> DIGIT_WIDTH;
    }
    ipi_trim(x);
}

// z = x * y
void ipi_umul(ipi_t *z, ipi_t *x, ipi_t *y){
    z->sign = x->sign * y->sign;
    z->size = x->size + y->size;
    z->digits = calloc(1, z->size);
    for (int i = 0; i < x->size; i++) {
        for (int j = 0, carry = 0; (j < y->size) || (carry > 0); j++) {
            udigit2_t next = z->digits[i+j] +
                (udigit2_t) x->digits[i] * (j < y->size ? y->digits[j] : 0) + carry;
            z->digits[i+j] = next;
            carry = next >> DIGIT_WIDTH;
        }
    }
    ipi_trim(z);
}

void ipi_mul(ipi_t *z, ipi_t *x, ipi_t *y){
	ipi_umul(z, x, y);
	z->sign = x->sign * y->sign;
}

// x, rem = x / y, x % y
void ipi_div_short(ipi_t *x, udigit_t y, udigit_t *rem){
    udigit2_t carry = 0;
    for (int i = x->size - 1; i >= 0; i--) {
        udigit2_t next = (carry << DIGIT_WIDTH) + x->digits[i];
        x->digits[i] = next / y;
        carry = next % y;
    }
    ipi_trim(x);
    *rem = carry;
}

// z = x / y, rem = x % y
void ipi_div(ipi_t *z, ipi_t *rem, ipi_t *x, ipi_t *y){
    udigit_t remainder;

    z->sign = x->sign * y->sign;
    if (y->size == 1) {
        ipi_copy(z, x, 0);
        ipi_div_short(z, y->digits[0], &remainder);
        ipi_from_int(rem, remainder);
    }
    else {
        // Do a couple easy cases
        int cmp = ipi_cmp(x, y);
        if (cmp < 0) {
            ipi_from_int(z, 0);
            ipi_copy(rem, x, 0);
            return;
        }
        if (cmp == 0) {
            ipi_from_int(z, 1);
            ipi_from_int(rem, 0);
            return;
        }

        // at this point x > y
        ipi_t q, n, z;
        ipi_from_int(&q, 0);
        ipi_copy(&n, x, y->size - 1);
        ipi_div_short(&n, y->digits[y->size - 1], &remainder);
        ipi_mul(&z, &n, y);
		ipi_copy(&n, x, 0);
		// ipi_sub(&n, x);

        printf("AFTER: %s %u\n", ipi_to_string(&n, 10), remainder);

        assert(false);
    }
}

bool ipi_from_string(ipi_t *ipi, char *s, int base){
    assert(base == 10);

    bool neg = false;
    ipi_from_int(ipi, 0);
    if (*s == '-') {
        ipi->sign = -1;
        s++;
    }
    else {
        ipi->sign = 1;
    }
    while (*s != 0) {
        ipi_mul_short(ipi, base);
        ipi_t next, sum;
        ipi_from_int(&next, *s - '0');
        ipi_uadd(&sum, ipi, &next);
		sum.sign = ipi->sign;
        ipi_release(&next);
        ipi_release(ipi);
        *ipi = sum;
        s++;
    }
    return true;
}

char *ipi_to_string(ipi_t *ipi, int base){
    assert(base == 10);
    char *s;

    if (ipi->size == 0) {
        s = malloc(2);
        strcpy(s, "0");
        return s;
    }
    
    ipi_t x;
    ipi_copy(&x, ipi, 0);

    int len = 1;
	s = malloc(1);
	*s = '\0';
    udigit_t rem;
    while (x.size != 0) {
        ipi_div_short(&x, base, &rem);
        s = realloc(s, len + 1);
        memmove(&s[1], s, len);
        s[0] = '0' + rem;
        len++;
    }
	if (x.sign < 0) {
        s = realloc(s, len + 1);
        memmove(&s[1], s, len);
        s[0] = '-';
	}
    ipi_release(&x);
    return s;
}

int main(int argc, char **argv){
    printf("Hello World %s %s\n", argv[1], argv[2]);

    ipi_t x, y, z, rem;
    ipi_from_string(&x, argv[1], 10);
    ipi_from_string(&y, argv[2], 10);
    printf("X"); ipi_dump(&x); printf("\n");
    printf("Y"); ipi_dump(&y); printf("\n");
	ipi_sub(&z, &x, &y);
    printf("Z"); ipi_dump(&z); printf(": %s\n", ipi_to_string(&z, 10));
	if (1) return 0;

    ipi_div(&z, &rem, &x, &y);
    printf("--> %s|%s\n", ipi_to_string(&z, 10), ipi_to_string(&rem, 10));
    return 0;
}
