

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b e)
(on c d)
(ontable d)
(on e c)
(clear a)
)
(:goal
(and
(on b c)
(on e d))
)
)


