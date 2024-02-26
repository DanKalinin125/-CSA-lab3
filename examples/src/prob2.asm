max_number:
  .word 4000000

a:
  .word 1

b:
  .word 1

result:
  .word 0

test_number:
  .word 1

out_addr:
  .word 3

_start:
  loop:
    mov r0, a
    mov r1, b
    add r0, r1  ; Нашли C = a + b

    mov r1, r0  ; Проверяем C максимальным числом
    mov r2, max_number
    sub r1, r2
    jg write_result  ; Если C - 4000000 > 0, то напечатать результат

    mov r1, r0  ; Проверяем четность C
    mov r2, test_number
    test r1, r2
    jnz finally  ; Если не 0, то C нечетное

    even:
      mov r1, r0
      mov r2, result
      add r1, r2
      mov result, r1  ; Перезаписываем результат как result = result + C

    finally:
      mov r1, b
      mov a, r1  ; a <- b
      mov b, r0  ; b <- c
      jmp loop

  write_result:
    mov r0, result
    mov (out_addr), r0
    hlt