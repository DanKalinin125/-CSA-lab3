org 10

message:
  .word 'Hello world!\0'

pointer:
  .word message

end_line:
  .word '\0'

out_address:
  .word 15

_start:
  loop:
    load (pointer)
    out out_address
    load pointer
    inc
    store pointer
    sub end_line
    jnz loop
