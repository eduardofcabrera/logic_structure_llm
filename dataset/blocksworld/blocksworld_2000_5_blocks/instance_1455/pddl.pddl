

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(on d c)
(on e a)
(clear d)
(clear e)
)
(:goal
(and
(on b d)
(on c b)
(on e a))
)
)


