

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c b)
(on d c)
(on e a)
(clear e)
)
(:goal
(and
(on a b)
(on b e)
(on c d)
(on d a))
)
)


