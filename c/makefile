BUILD_DIR = ./build

all: main

main: link
link: compile

compile:
	$(MAKE) --directory=./src

link:
	gcc -o main $(BUILD_DIR)/*.o	 

clean:
	rm -fv $(BUILD_DIR)/*

.PHONY: clean
