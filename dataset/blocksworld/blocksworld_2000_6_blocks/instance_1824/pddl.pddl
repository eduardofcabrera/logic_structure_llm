

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b a)
(on c b)
(on d c)
(ontable e)
(clear d)
)
(:goal
(and
(on a c)
(on c d)
(on d b)
(on e a))
)
)


