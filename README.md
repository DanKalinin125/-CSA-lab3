# Архитектура компьютера - Лаб 3

## Автор

> Калинин Даниил Дмитриевич, P33141

## Вариант (с упрощением)

> Исходный вариант: alg | risc | neum | hw | instr | binary | stream | mem | cstr | prob2 | pipeline\
> **Вариант после упрощения**:  asm | risc | neum | hw | instr | struct | stream | mem | cstr | prob2

### Описание варианта

- **asm** - язык программирования синтаксис ассемблера. Необходима поддержка label-ов.
- **risc** - система команд должна быть упрощенной, в духе RISC архитектур:
  - стандартизированная длина команд;
  - операции над данными осуществляются только в рамках регистров;
  - доступ к памяти и ввод-вывод -- отдельные операции (с учётом специфики вашего варианта mem/port);
- **neum** - фон Неймановская архитектура организация памяти
- **hw** - hardwired. Реализуется как часть модели.
- **instr** - процессор необходимо моделировать с точностью до каждой инструкции (наблюдается состояние после каждой инструкции).
- **struct** - машинный код в виде высокоуровневой структуры данных. Считается, что одна инструкция укладывается в одно машинное слово.
- **stream** - ввод-вывод осуществляется как поток токенов. Есть в примере. Логика работы:
  - при старте модели у вас есть буфер, в котором представлены все данные ввода (['h', 'e', 'l', 'l', 'o']);
  - при обращении к вводу (выполнение инструкции) модель процессора получает "токен" (символ) информации;
  - если данные в буфере кончились -- останавливайте моделирование;
  - вывод данных реализуется аналогично, по выполнении команд в буфер вывода добавляется ещё один символ;
  - по окончании моделирования показать все выведенные данные;
  - логика работы с буфером реализуется в рамках модели на Python.
- **mem** - memory-mapped (порты ввода-вывода отображаются в память и доступ к ним осуществляется штатными командами),
  - отображение портов ввода-вывода в память должно конфигурироваться (можно hardcode-ом).
- **cstr** - Null-terminated (C string)
- **prob2** - Even Fibonacci numbers (сумма четных чисел Фибонначи, не превышающих 4 млн).

## Язык программирования

Язык программирования должен поддерживать:

- ветвления
- циклы
- математику
- строки (Null-terminated (C string))
- ввод/вывод
- label-ы

### Форма Бэкуса — Наура

```ebnf
// Команды и прочие элементы языка программирования

<program> ::= <program_line> | <program_line> "\n" <program>

<program_line> ::= <code_line> | <comment> | <code_line> <comment>

<code_line> ::= <address_definition> | <data_definition> | <label_definition> | <command>

<address_definition> ::= "org" <non_neg_number>

<data_definition> ::= <label_definition> "\n" <data>

<data> ::= ".word" <number> | ".word" <string> | ".word" <label_name>

<command> ::= <onear_instruction> <address> | <branch_instruction> <address> | <nullar_instruction>

<address> = <label_name> | "(" <label_name> ")"

<label_definition> ::= <label_name> ":"

<label_name> ::= <word> 

<branch_instruction> ::= "jg" | "jz" | "jnz" | "jmp"

<one_parameter_instruction> ::= "load" | "store" | "add" | "sub"

<zero_parameters_instruction> ::= "inc" | "dec" | "hlt" 

<comment> ::= ";" <text>

// Строки

<string> ::= '"' <text> '"'

<text> ::= <word> | <word> <word>

<word> ::= <character> | <character> <word>

<character> ::= <symbol> | <letter> | <digit>

// Числа

<number> ::= [-] <non-negative number>

<non-negative number> ::= <digit> | <digit> <non-negative number>

// Основные термы

<symbol> ::=  "|" | " " | "-" | "!" | ...

<letter> ::= "a" | "b" | "c" | ... | "z" | "A" | "B" | "C" | ... | "Z"

<digit> ::= "0" | "1" | "2" |  ... | "9"
```

Строке программы может соответствовать:

- Пустая строка 
- Комментарий `<comment>`
- Определение адреса `<address_definition> = org + Не отрицательное число (Адрес)`
- Определение метки `<label_definition>`
- Определение данных `<data_definition> = <label_definition> + .word + Данные (число или строка)`
  - Здесь, конечно, 2 строки, но определение данных без обозначения метки не имеет смысла
- Команда `<command> = Инструкция + Адрес (если его наличие предусматривает инструкция)`

### Семантика

- Глобальная видимость данных
- Поддерживаются целочисленные литералы (без ограничений на размер)
- Поддерживаются строковые литералы в виде C-string
  - Пример объявления строковых данных: .word 'Hello\0'
- Код выполняется последовательно
- Точка входа в программу -- метка _start (метка не может повторяться или отсутствовать)
- Название метки не должно:
  - совпадать с названием команды
  - начинаться с цифры
  - совпадать с ключевыми словами org или .word
- Метки располагаются на строке, предшествующей строке с командой, операнды находятся на одной строке с командами
- Пробельные символы в конце и в начале строки игнорируются
- Любой текст, расположенный в конце строки после символа ; трактуется как комментарий
- Память выделяется статически, при запуске модели.

## Организация памяти

```
Registers
+------------------------------------+
| AC - аккумулятор                   |
+------------------------------------+
| DR - регистр данных                |
+------------------------------------+
| IR - регистр инструкции            |
+------------------------------------+
| IP - счётчик команд                |
+------------------------------------+
| SP - указатель стека               |
+------------------------------------+
| AR - адрес записи в память         |
+------------------------------------+
| PS - состояние программы           |
+------------------------------------+
| BR - буфферный регистр             |
+------------------------------------+

Instruction & Data memory
+-----------------------------------------------+
|    0    :  jmp _start                         |
|    1    :  interruption vector                |
|        ...                                    |
| _start  :  program start                      |
|        ...                                    |
|    i    :  interruption handler               |
|        ...                                    |
+-----------------------------------------------+
```

1. Память данных и команд общая (фон Нейман)
2. Слова знаковые
3. Размер машинного слова не определен (достаточно, чтобы влезало число для prob2)
4. Размер адреса = **16 бит**, следовательно, в памяти и в стеке по **65536 ячеек памяти** в каждом.
5. Стек растет сверху вниз (от 00 и до FF)
6. Адрес **0** зарезервирован для перехода к началу программы
7. Адрес **1** зарезервирован для указания адреса подпрограммы обработки прерывания ввода
8. Виды адресации: **абсолютная** и **косвенная**

## Система команд

### Безадресные команды

|Код|Команда|N|Z|V|C|Описание|Семантика|
|-|-|-|-|-|-|-|-|
|00| hlt |-|-|-|-| Останов | |
|01| inc |*|*|*|*| Инкремент | AC + 1 -> AC |
|02| dec |*|*|*|*| Декримент | AC - 1 -> AC |
|03| pop |*|*|0|-| Снять со вершины стека | (SP) -> AC; SP - 1 -> SP |
|04| push |-|-|-|-| Положить на стек | SP + 1 -> SP; AC -> (SP) |
|05| iret |*|*|*|*| Возврат из прерывания | (SP) -> PS; (SP) -> IP |

### Команды ввода-вывода

|Код|Команда|N|Z|V|C|Описание|Семантика|
|-|-|-|-|-|-|-|-|
|06| di |-|-|-|-| Запрет прерываний | |
|07| ei |-|-|-|-| Разрешение прерываний | |

### Адресные команды

|Код|Команда|N|Z|V|C|Описание|Семантика|
|-|-|-|-|-|-|-|-|
|08| add M |*|*|*|*| Сумма аккумулятора с M | AC + M -> AC |
|09| sub M |*|*|*|*| Разница аккумулятора с M | AC - M -> AC |
|0A| load M |*|*|0|-| Загрузить M в аккумулятор | M -> AC |
|0B| store M |-|-|-|-| Загрузить аккумулятор в M | AC -> M |
|0C| jmp M |-|-|-|-| Перейти к адресу M | M -> IP |

### Команды ветвления

|Код|Команда|N|Z|V|C|Описание|Семантика|
|-|-|-|-|-|-|-|-|
|0D| jg M |-|-|-|-| Перейти по адресу, если флаг N == 0 | |
|0E| jz M |-|-|-|-| Перейти по адресу, если флаг Z == 0 | |
|0F| jnz M |-|-|-|-| Перейти по адресу, если флаг Z != 0 | |
