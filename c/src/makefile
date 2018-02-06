BUILD_DIR = ../build

all: compile

compile: main simulation utilities

main:
	gcc -c main.c -o $(BUILD_DIR)/main.o

simulation:
	$(MAKE) --directory=./simulation

utilities:
	$(MAKE) --directory=./utilities

.PHONY: simulation utilities
