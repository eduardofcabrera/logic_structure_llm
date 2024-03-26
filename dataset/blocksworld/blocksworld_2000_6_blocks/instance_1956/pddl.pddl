

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c b)
(on d c)
(ontable e)
(clear a)
(clear e)
)
(:goal
(and
(on a d)
(on b c)
(on d b)
(on e a))
)
)


