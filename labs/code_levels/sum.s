// 1부터 100까지 더해서 화면에 출력 (macOS · arm64)
.global _main
.align 4
_main:
    mov     x1, #0              // 합계 = 0
    mov     x2, #1              // n = 1
loop:
    add     x1, x1, x2          // 합계 += n
    add     x2, x2, #1          // n += 1
    cmp     x2, #100
    b.le    loop                // n <= 100 이면 반복
    adrp    x3, buf@PAGE        // 숫자 → 글자
    add     x3, x3, buf@PAGEOFF
    add     x3, x3, #15
    mov     w4, #10             // 줄바꿈
    strb    w4, [x3]
    mov     x5, #10
digit:
    udiv    x6, x1, x5
    msub    x7, x6, x5, x1      // 나머지 = 마지막 자리
    add     x7, x7, #48         // '0' 글자로
    sub     x3, x3, #1
    strb    w7, [x3]
    mov     x1, x6
    cbnz    x1, digit
    mov     x0, #1              // 화면(표준 출력)
    mov     x1, x3
    adrp    x2, buf@PAGE
    add     x2, x2, buf@PAGEOFF
    add     x2, x2, #16
    sub     x2, x2, x3          // 글자 수
    mov     x16, #4             // 시스템 호출 4번 = write
    svc     #0x80
    mov     x0, #0
    mov     x16, #1             // 시스템 호출 1번 = exit
    svc     #0x80
.data
buf: .space 16
