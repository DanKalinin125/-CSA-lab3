org 10

message:
  .word 'Hello world!'

pointer:
  .word message

end_str:
  .word '\0'

out_addr:
  .word 2

_start:
  mov r0, (pointer)
  mov (out_addr), r0
  mov r0, pointer
  inc r0
  mov pointer, r0
  sub r0, end_str
  jnz _start
  hlt
