

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c d)
(on d b)
(on e a)
(clear c)
)
(:goal
(and
(on c b)
(on e c))
)
)


