

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c e)
(ontable d)
(ontable e)
(clear a)
(clear b)
(clear c)
(clear d)
)
(:goal
(and
(on e b))
)
)


