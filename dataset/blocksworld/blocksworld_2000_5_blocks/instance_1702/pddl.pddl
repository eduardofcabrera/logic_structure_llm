

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
(on a e)
(on b c)
(on c a)
(on d b))
)
)


