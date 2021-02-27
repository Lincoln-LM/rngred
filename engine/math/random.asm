Random_::
; Generate a random 16-bit value.
	ldh a, [hUnusedCoinsByte] ; UnusedCoinsByte is used as a check for if random has been called yet.
	cp 0					  ; Check if random has been called, 
	jr z,.start               ; if not set up initial seeds.
	ldh a, [hRandomSub]		  ; Load current Sub value,
	call MultBy5		      ; multiply it by 5, (LCRNG)
	add 13					  ; add 13.			  (LCRNG)
	cp 100					  ; Check if sub value is the value before the initial (advance 255 from Sub initial)
	jr z,.endPeriod			  ; if it is, end the rng period 1 early, this is used to ensure the Sub RNG period is 1 less than the Add RNG period.
	ldh [hRandomSub], a       ; Set new Sub value.
	ldh a, [hRandomAdd]		  ; Load current Add value,
	call MultBy5			  ; (LCRNG)
	add 13					  ; (LCRNG)
	ldh [hRandomAdd], a		  ; Set new Add value.
	ret

.start
; Generate first random 16-bit value, used to set initial.
	ld a, 1					  ; Used to set random check and Sub initial.
	ldh [hUnusedCoinsByte], a ; Set check for if random has been called.
	call MultBy5			  ; (LCRNG)
	add 13					  ; (LCRNG)
	ldh [hRandomSub], a		  ; Set new Sub value.
	ld a, 0					  ; Set Add initial,
	call MultBy5			  ; (LCRNG)
	add 13					  ; (LCRNG)
	ldh [hRandomAdd], a		  ; Set new Add value.
	ret

.endPeriod
; End RNG period 1 early.
	ld a, 1					  ; Set to Sub initial,
	ldh [hRandomSub], a		  ; set Sub initial.
	ldh a, [hRandomAdd]		  ; Load current Add value,
	call MultBy5			  ; (LCRNG)
	add 13      			  ; (LCRNG)
	ldh [hRandomAdd], a		  ; Set new Add value.
	ret

MultBy5::
; Multiply a by 5.
	ld b,a	; b = a
	SLA b
	SLA b   ; b = b<<2
	ADD a,b ; a += b
	ret
