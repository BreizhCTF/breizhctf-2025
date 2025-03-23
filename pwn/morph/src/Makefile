CC = gcc
CFLAGS = -Wall -Wextra -O2 -static
TARGET = metamorph

all: $(TARGET)

$(TARGET): metamorph.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(TARGET)

.PHONY: all clean
