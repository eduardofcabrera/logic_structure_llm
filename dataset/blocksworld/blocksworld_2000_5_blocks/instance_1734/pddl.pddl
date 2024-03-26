

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c b)
(ontable d)
(on e c)
(clear a)
(clear d)
)
(:goal
(and
(on a e)
(on c d)
(on e c))
)
)


