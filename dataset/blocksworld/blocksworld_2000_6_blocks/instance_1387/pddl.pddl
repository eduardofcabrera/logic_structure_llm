

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c b)
(on d c)
(on e a)
(clear d)
)
(:goal
(and
(on a b)
(on b d)
(on c e)
(on d c))
)
)


