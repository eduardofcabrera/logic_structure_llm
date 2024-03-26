

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c b)
(ontable d)
(on e a)
(clear c)
(clear d)
)
(:goal
(and
(on a e)
(on b d))
)
)


