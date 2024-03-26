

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b e)
(on c b)
(ontable d)
(ontable e)
(clear a)
(clear c)
)
(:goal
(and
(on e d))
)
)


