BUILD_DIR = ../../build

all: $(BUILD_DIR)/list.o $(BUILD_DIR)/random.o

$(BUILD_DIR)/%.o: %.c %.h
	gcc -c $< -o $@
