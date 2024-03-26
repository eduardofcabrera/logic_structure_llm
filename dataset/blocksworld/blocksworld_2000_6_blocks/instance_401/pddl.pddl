

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b e)
(on c b)
(on d a)
(ontable e)
(clear d)
)
(:goal
(and
(on c d)
(on e a))
)
)


