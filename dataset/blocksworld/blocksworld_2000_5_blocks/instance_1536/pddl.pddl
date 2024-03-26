

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c b)
(on d c)
(ontable e)
(clear a)
(clear d)
)
(:goal
(and
(on a e)
(on d a)
(on e b))
)
)


