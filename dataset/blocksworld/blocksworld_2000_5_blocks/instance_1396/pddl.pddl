

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c a)
(on d b)
(on e c)
(clear d)
)
(:goal
(and
(on a e)
(on b a)
(on c b))
)
)


