(define nil ())

(define (sort x)
  (if (null? (cdr x))
      x
      (min (car x) (cdr x) nil)))

(define (min x items rest)
  (cond ((null? items)
         (cons x (sort rest)))
        ((<= x (car items))
         (min x (cdr items) (append rest (list (car items)))))
        (else (min (car items) (append rest (cdr items)) (list x)))))
