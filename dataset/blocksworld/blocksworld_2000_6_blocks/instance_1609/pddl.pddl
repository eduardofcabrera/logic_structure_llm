

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear b)
(clear c)
)
(:goal
(and
(on a c)
(on b e)
(on e a))
)
)


