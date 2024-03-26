

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b e)
(on c b)
(ontable d)
(on e a)
(clear c)
)
(:goal
(and
(on b e)
(on e c))
)
)


