tests:
	@make extra --no-print-directory
	@python3 testfiles/test.py
	@make clean --no-print-directory
interpret:
	@make extra --no-print-directory
	@python3 src/junior.py
	@make clean --no-print-directory
extra:
	@python3 tools/ast_generator.py
clean:
	@rm -r src/__pycache__
