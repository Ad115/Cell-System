BUILD_DIR = ../../../build

all: $(BUILD_DIR)/cell_line.o cell

$(BUILD_DIR)/%.o: %.c %.h
	gcc -c $< -o $@

cell: 
	 $(MAKE) --directory=$@

.PHONY: cell
