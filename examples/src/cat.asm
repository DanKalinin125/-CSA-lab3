end_str:
  .word 0

in_addr:
  .word 1

out_addr:
  .word 2

_start:
  mov r0, (in_addr)
  mov r1, r0
  mov r2, end_str
  sub r1, r2
  jnz write
  hlt

write:
  mov (out_addr), r0
  jmp _start


