

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c e)
(on d c)
(on e b)
(clear d)
)
(:goal
(and
(on b e)
(on e d))
)
)


