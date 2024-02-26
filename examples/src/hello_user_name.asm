first_message:
  .word 'What is your name?'

second_message:
  .word 'Hello, '

exclamation_point:
  .word '!'

pointer:  ; Адрес печатаемого символа
  .word 0

end_str:
  .word 0

in_addr:
  .word 1

out_addr:
  .word 2

_start:

  write_first_message:  ; Пишем первое сообщение
    mov r0, first_message
    mov pointer, r0  ; Кладем в pointer указатель на первый символ первого сообщения

    load_first_message_char:
      mov r0, (pointer)
      mov r1, r0
      mov r2, end_str
      sub r1, r2
      jnz write_first_message_char
      jmp read_name

    write_first_message_char:
      mov (out_addr), r0
      mov r0, pointer
      inc r0
      mov pointer, r0
      jmp load_first_message_char

  read_name:
    mov r0, name
    mov pointer, r0  ; Кладем в pointer указатель на первый символ имени

    read_name_char:
      mov r0, (in_addr)

    store_name_char:
      mov (pointer), r0
      mov r1, end_str
      sub r0, r1
      jz write_second_message
      mov r0, pointer
      inc r0
      mov pointer, r0
      jmp read_name_char

  write_second_message:  ; Пишем второе сообщение
    mov r0, second_message
    mov pointer, r0  ; Кладем в pointer указатель на первый символ второго сообщения

    load_second_message_char:
      mov r0, (pointer)
      mov r1, r0
      mov r2, end_str
      sub r1, r2
      jnz write_second_message_char
      jmp write_name

    write_second_message_char:
      mov (out_addr), r0
      mov r0, pointer
      inc r0
      mov pointer, r0
      jmp load_second_message_char

  write_name:  ; Пишем имя
    mov r0, name
    mov pointer, r0  ; Кладем в pointer указатель на первый символ имени

    load_name_char:
      mov r0, (pointer)
      mov r1, r0
      mov r2, end_str
      sub r1, r2
      jnz write_name_char
      jmp write_exclamation_point

    write_name_char:
      mov (out_addr), r0
      mov r0, pointer
      inc r0
      mov pointer, r0
      jmp load_name_char

  write_exclamation_point:  ; Пишем восклицательный знак
    mov r0, (exclamation_point)
    mov (out_addr), r0
    hlt

name:
  .word 0