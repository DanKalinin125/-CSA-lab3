first_message:
  .word 'What is your name?'

second_message:
  .word 'Hello, '

exclamation_point:
  .word '!'

first_message_pointer:
  .word first_message

second_message_pointer:
  .word second_message

read_name_pointer:
  .word name

write_name_pointer:
  .word name

end_str:
  .word 0

in_addr:
  .word 1

out_addr:
  .word 2

_start:

  write_first_message:  ; Пишем первое сообщение
    load_first_message_char:
      mov r0, (first_message_pointer)
      mov r1, r0
      mov r2, end_str
      sub r1, r2
      jnz write_first_message_char
      jmp read_name

    write_first_message_char:
      mov (out_addr), r0
      mov r0, first_message_pointer
      inc r0
      mov first_message_pointer, r0
      jmp load_first_message_char

  read_name:
    read_name_char:
      mov r0, (in_addr)

    store_name_char:
      mov (read_name_pointer), r0
      mov r1, end_str
      sub r0, r1
      jz write_second_message
      mov r0, read_name_pointer
      inc r0
      mov read_name_pointer, r0
      jmp read_name_char

  write_second_message:  ; Пишем второе сообщение
    load_second_message_char:
      mov r0, (second_message_pointer)
      mov r1, r0
      mov r2, end_str
      sub r1, r2
      jnz write_second_message_char
      jmp write_name

    write_second_message_char:
      mov (out_addr), r0
      mov r0, second_message_pointer
      inc r0
      mov second_message_pointer, r0
      jmp load_second_message_char

  write_name:  ; Пишем имя
    load_name_char:
      mov r0, (write_name_pointer)
      mov r1, r0
      mov r2, end_str
      sub r1, r2
      jnz write_name_char
      jmp write_exclamation_point

    write_name_char:
      mov (out_addr), r0
      mov r0, write_name_pointer
      inc r0
      mov write_name_pointer, r0
      jmp load_name_char

  write_exclamation_point:  ; Пишем восклицательный знак
    mov r0, exclamation_point
    mov (out_addr), r0
    hlt

name:
  .word 0