# Harvey Mudd College VLSI MIPS Project
# Matt McKnett
# Spring, 2007
# 
# Bootloader bootstrap code
#
# This code is step 1 in the bootloading process.  It is designed to jump
# to the main boot code that is stored in ROM.  This keeps the bootloader code
# from running into exception entry points and gives us a simple test of CPU
# function (according to See MIPS Run page 110). 

# We don't want the assembler to reorder or fill branch delay slots.
.set noreorder
.text

reset:
	j	load
	nop

load:
	# Boot-loading code goes here.
	syscall	0x0
	j	load
	nop

# Originally, we were going to jump to a location to prove that the processor is
# configured enough to handle it, but it is probably best to simply jump to the 
# next instruction (which will be the loader) as above.
#boot:	lui $8, 0xBFC0		# Our main bootloader is located at 0xBFC00E00
#	ori $8, $8, 0x0E00
#	jr  $8
#	nop

#	b	reset		# For now, we will try getting the linker
#				# to use the boot_loader tag __reset
