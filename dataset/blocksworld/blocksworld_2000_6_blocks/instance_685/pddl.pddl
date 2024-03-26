

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(ontable c)
(ontable d)
(on e b)
(clear a)
(clear d)
(clear e)
)
(:goal
(and
(on b e)
(on c a))
)
)


