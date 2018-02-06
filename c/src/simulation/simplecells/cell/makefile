BUILD_DIR = ../../../../build

all: $(BUILD_DIR)/cell.o $(BUILD_DIR)/cell_action.o $(BUILD_DIR)/action_result.o

$(BUILD_DIR)/%.o: %.c %.h
	gcc -c $< -o $@
