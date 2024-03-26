

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(on c b)
(ontable d)
(ontable e)
(clear a)
(clear c)
)
(:goal
(and
(on c e)
(on e d))
)
)


