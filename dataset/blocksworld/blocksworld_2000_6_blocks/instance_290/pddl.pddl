

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b c)
(on c e)
(ontable d)
(on e d)
(clear a)
)
(:goal
(and
(on a e)
(on c d))
)
)


