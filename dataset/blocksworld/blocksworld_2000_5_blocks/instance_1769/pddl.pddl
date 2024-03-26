

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear b)
(clear e)
)
(:goal
(and
(on a b)
(on b e)
(on e c))
)
)


