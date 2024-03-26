

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(on c d)
(ontable d)
(on e c)
(clear a)
(clear e)
)
(:goal
(and
(on a e)
(on c a)
(on e d))
)
)


