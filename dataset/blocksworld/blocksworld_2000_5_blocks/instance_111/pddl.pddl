

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b a)
(ontable c)
(on d c)
(on e d)
(clear b)
)
(:goal
(and
(on b c)
(on c d)
(on d e))
)
)


