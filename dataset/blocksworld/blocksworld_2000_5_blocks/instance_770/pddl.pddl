

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(on c b)
(ontable d)
(on e a)
(clear e)
)
(:goal
(and
(on a d)
(on b c)
(on c e)
(on d b))
)
)


