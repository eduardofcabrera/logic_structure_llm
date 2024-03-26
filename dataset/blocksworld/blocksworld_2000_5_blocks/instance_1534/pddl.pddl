

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(on c b)
(ontable d)
(on e a)
(clear d)
(clear e)
)
(:goal
(and
(on b e)
(on c d)
(on d b)
(on e a))
)
)


