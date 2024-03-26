

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on c e)
(on e a))
)
)


