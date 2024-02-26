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
  mov r1, r0
  mov r2, end_str
  sub r1, r2
  jnz write
  hlt

write:
  mov (out_addr), r0
  mov r0, pointer
  inc r0
  mov pointer, r0
  jmp _start

