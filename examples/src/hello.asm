message:
  .word 'Hello world!' ; Наше сообщение

; Указатель на следующий символ для печати
pointer:
  .word message

end_str:
  .word 0

out_addr:
  .word 2

_start:
  mov r0, (pointer)
  mov (out_addr), r0
  mov r0, pointer
  inc r0
  mov pointer, r0
  mov r1, end_str
  sub r0, r1
  jnz _start
  hlt
